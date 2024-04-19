import json

import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.services.user_service import UserService
from .serializers.order_serializer import OrderInputSerializer
from .serializers.order_serializer import OrderOutputSerializer
from .serializers.plan_serializer import PlanOutputSerializer
from .serializers.user_subscription_serializer import UserSubscriptionInputSerializer, UserSubscriptionUpdateSerializer
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


class GetInvoice(APIView):
    permission_classes = (IsAuthenticated,)
    _order_service = OrderService()

    def get(self, request, pk):
        order = self._order_service.get_order_details(pk, request.user.id)

        try:
            invoice_data = stripe.Invoice.retrieve(order.invoice_id)
            return Response({"message": invoice_data.hosted_invoice_url}, status=status.HTTP_200_OK)

        except Exception as e:
            raise e


class CancelSubscription(APIView):
    permission_classes = (IsAuthenticated,)

    _user_service = UserSubscriptionService()

    def post(self, request):
        user_current_plan = self._user_service.get_current_subscription_by_user(request.user)

        if user_current_plan and user_current_plan.status == "CANCELED":
            return Response(
                {"message": "You already canceled your subscription"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_current_plan and user_current_plan.status != "ACTIVE":
            return Response(
                {"message": "You don't have an active subscription"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            stripe.Subscription.cancel(user_current_plan.subscription_id)

            # Update UserSubscription object
            user_subscription_update_data = {
                "status": "CANCELED",
            }
            user_subscription_update_serializer = UserSubscriptionUpdateSerializer(data=user_subscription_update_data)
            user_subscription_update_serializer.is_valid(raise_exception=True)
            self._user_service.partial_update(
                user_current_plan.pk,
                user_subscription_update_serializer.validated_data
            )

        except Exception as e:
            raise e

        return Response(status=status.HTTP_200_OK)


class CreateSubscription(APIView):
    permission_classes = (IsAuthenticated,)

    _service = UserSubscriptionService()
    _plan_service = PlanService()

    def post(self, request):
        user_current_plan = self._service.get_current_subscription_by_user(request.user)

        if user_current_plan:
            if user_current_plan.status == "ACTIVE" or self._service.subscription_is_valid(user_current_plan):
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
    _user_service = UserService()

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

                # Create Order object
                object_data = event.get("data").get("object")
                customer_details_data = object_data.get("customer_details")
                data = {
                    "currency": object_data.get("currency"),
                    "customer": object_data.get("customer"),
                    "city": customer_details_data.get("address").get("city"),
                    "country": customer_details_data.get("address").get("country"),
                    "line1": customer_details_data.get("address").get("line1"),
                    "line2": customer_details_data.get("address").get("line2"),
                    "postal_code": customer_details_data.get("address").get("postal_code"),
                    "state": customer_details_data.get("address").get("state"),
                    "email": customer_details_data.get("email"),
                    "name": customer_details_data.get("name"),
                    "phone": customer_details_data.get("phone"),
                    "total_amount": object_data.get("amount_total"),
                    "invoice_id": object_data.get("invoice"),
                }
                order_serializer = OrderInputSerializer(data=data)
                order_serializer.is_valid(raise_exception=True)
                order = self._order_service.create(order_serializer.validated_data, user_subscription.user)

                # Update UserSubscription object
                user_subscription_update_data = {
                    "status": "ACTIVE",
                    "order": order.pk,
                    "subscription_id": object_data.get("subscription")
                }
                user_subscription_update_serializer = UserSubscriptionUpdateSerializer(
                    data=user_subscription_update_data
                )
                user_subscription_update_serializer.is_valid(raise_exception=True)
                self._user_subscription_service.partial_update(
                    user_subscription.pk,
                    user_subscription_update_serializer.validated_data
                )

        elif event_type == 'invoice.paid':
            pass

        elif event_type == 'invoice.payment_failed':
            if event:
                # Update UserSubscription object

                user_id = event.get("data").get("object").get("metadata").get("user_id")
                user_subscription = self._user_subscription_service.get_current_subscription_by_user(int(user_id))
                user_subscription_update_data = {
                    "status": "ACTIVE",
                }
                user_subscription_update_serializer = UserSubscriptionUpdateSerializer(
                    data=user_subscription_update_data
                )
                user_subscription_update_serializer.is_valid(raise_exception=True)
                self._user_subscription_service.partial_update(
                    user_subscription.pk,
                    user_subscription_update_serializer.validated_data
                )
        else:
            pass

        return JsonResponse(data={"status": "success"})
