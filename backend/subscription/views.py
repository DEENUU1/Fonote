import json

import stripe
from django.conf import settings
from django.contrib.auth.backends import UserModel
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers.order_serializer import OrderInputSerializer
from .serializers.order_serializer import OrderOutputSerializer
from .serializers.plan_serializer import PlanOutputSerializer
from .serializers.user_subscription_serializer import UserSubscriptionInputSerializer
from .services.order_service import OrderService
from .services.plan_service import PlanService
from .services.user_subscription_service import UserSubscriptionService

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET


class PlanListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        plans = PlanService().get_active_plan_list()
        return Response(PlanOutputSerializer(plans, many=True).data, status=status.HTTP_200_OK)


class OrderListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        orders = OrderService().get_order_list_by_user(request.user)
        return Response(OrderOutputSerializer(orders, many=True).data, status=status.HTTP_200_OK)


class OrderDetailsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        order = OrderService().get_order_details(pk, request.user.id)
        return Response(OrderOutputSerializer(order).data, status=status.HTTP_200_OK)


class CancelSubscription(APIView):
    permission_classes = (IsAuthenticated,)

    _user_service = UserSubscriptionService()

    def post(self, request):
        user_current_plan = self._user_service.get_current_subscription_by_user(request.user)

        if user_current_plan and user_current_plan.status != "ACTIVE":
            return Response(
                {"message": "You don't have an active subscription"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            stripe.Subscription.cancel(user_current_plan.subscription_id)
            self._user_service.change_status(user_current_plan.pk, "CANCELED")
        except Exception as e:
            raise e

        return Response(status=status.HTTP_200_OK)


class CreateSubscription(APIView):
    permission_classes = (IsAuthenticated,)

    _service = UserSubscriptionService()
    _plan_service = PlanService()

    def post(self, request):
        user_current_plan = self._service.get_current_subscription_by_user(request.user)

        if user_current_plan and user_current_plan.status == "ACTIVE":
            return Response(
                {"message": "User already have active subscription"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': data['price_id'],
                        'quantity': 1
                    }
                ],
                metadata={
                    "user_id": request.user.id
                },
                mode='subscription',
                success_url=settings.FRONTEND_SUBSCRIPTION_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.FRONTEND_SUBSCRIPTION_CANCEL_URL,
            )

            plan = self._plan_service.get_plan_by_price_id(data["price_id"])
            serializer = UserSubscriptionInputSerializer(
                data={
                    "session_id": checkout_session.id,
                    "plan": plan.pk,
                }
            )
            serializer.is_valid(raise_exception=True)
            self._service.create(serializer.validated_data, request.user)

            return Response(data=checkout_session.url, status=status.HTTP_200_OK)

        except Exception as err:
            raise err


class WebHook(APIView):
    _user_subscription_service = UserSubscriptionService()
    _order_service = OrderService()

    def post(self, request):
        """
            This API handling the webhook .

            :return: returns event details as json response .
        """
        request_data = json.loads(request.body)
        event = None

        if webhook_secret:
            signature = request.META['HTTP_STRIPE_SIGNATURE']
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.body,
                    sig_header=signature,
                    secret=webhook_secret
                )

            except ValueError as err:
                raise err
            except stripe.error.SignatureVerificationError as err:
                raise err

            event_type = event['type']
        else:
            event_type = request_data['type']

        if event_type == 'checkout.session.completed':
            if event:
                user_id = event.get("data").get("object").get("metadata").get("user_id")
                user_subscription = self._user_subscription_service.get_current_subscription_by_user(int(user_id))

                data = {
                    "currency": event.get("data").get("object").get("currency"),
                    "customer": event.get("data").get("object").get("customer"),
                    "city": event.get("data").get("object").get("customer_details").get("address").get("city"),
                    "country": event.get("data").get("object").get("customer_details").get("address").get("country"),
                    "line1": event.get("data").get("object").get("customer_details").get("address").get("line1"),
                    "line2": event.get("data").get("object").get("customer_details").get("address").get("line2"),
                    "postal_code": event.get("data").get("object").get("customer_details").get("address").get(
                        "postal_code"),
                    "state": event.get("data").get("object").get("customer_details").get("address").get("state"),
                    "email": event.get("data").get("object").get("customer_details").get("email"),
                    "name": event.get("data").get("object").get("customer_details").get("name"),
                    "phone": event.get("data").get("object").get("customer_details").get("phone"),
                    # "stripe_id": ...,  # TODO: stripe_id
                    "total_amount": event.get("data").get("object").get("amount_total"),
                    # "invoice_url": ...,  # TODO: invoice_url
                    "invoice_id": event.get("data").get("object").get("invoice"),
                }
                order_serializer = OrderInputSerializer(data=data)
                order_serializer.is_valid(raise_exception=True)

                user = UserModel.objects.get(id=user_id)

                order = self._order_service.create(order_serializer.validated_data, user)
                self._user_subscription_service.change_status(user_subscription.pk, "ACTIVE")
                self._user_subscription_service.set_order_object(user_subscription.pk, order)
                self._user_subscription_service.set_subscription_id(
                    user_subscription.pk,
                    event.get("data").get("object").get("subscription")
                )
        elif event_type == 'invoice.paid':
            print("Paid")
            print("Add this later - works only in production mode")

        elif event_type == 'invoice.payment_failed':
            if event:
                user_id = event.get("data").get("object").get("metadata").get("user_id")
                user_subscription = self._user_subscription_service.get_current_subscription_by_user(int(user_id))
                self._user_subscription_service.change_status(user_subscription.pk, "FAILED")
        else:
            pass

        return JsonResponse(data={"status": "success"})
