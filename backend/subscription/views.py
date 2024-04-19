import json

import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.plan_service import PlanService
from .services.user_subscription_service import UserSubscriptionService
from .serializers.user_subscription_serializer import UserSubscriptionInputSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET


class PlanListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        plans = PlanService().get_active_plan_list()
        return Response(plans, status=status.HTTP_200_OK)


class CreateSubscription(APIView):
    permission_classes = (IsAuthenticated,)

    _service = UserSubscriptionService()
    _plan_service = PlanService()

    def post(self, request):
        user_current_plan = self._service.get_current_subscription_by_user(request.user)

        if user_current_plan.get("status") == "ACTIVE":
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
                metadata = {
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
                    "plan": plan.get("id")
                }
            )
            serializer.is_valid(raise_exception=True)
            self._service.create(serializer.validated_data, request.user)

            return Response(data=checkout_session.url, status=status.HTTP_200_OK)

        except Exception as err:
            raise err


class WebHook(APIView):
    _user_subscription_service = UserSubscriptionService()

    def post(self, request):
        """
            This API handling the webhook .

            :return: returns event details as json response .
        """
        request_data = json.loads(request.body)
        event = None

        with open("request_data.txt", "w") as file:
            file.write(str(request_data))

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
                self._user_subscription_service.change_status(user_subscription.get("id"), "ACTIVE")
                # Create order object here
        elif event_type == 'invoice.paid':
            if event:

                user_id = event.get("data").get("object").get("metadata").get("user_id")
                user_subscription = self._user_subscription_service.get_current_subscription_by_user(int(user_id))
                self._user_subscription_service.change_status(user_subscription.get("id"), "PAID")
                # Update invoice here
        elif event_type == 'invoice.payment_failed':
            if event:
                user_id = event.get("data").get("object").get("metadata").get("user_id")
                user_subscription = self._user_subscription_service.get_current_subscription_by_user(int(user_id))
                self._user_subscription_service.change_status(user_subscription.get("id"), "FAILED")
        else:
            pass

        return JsonResponse(data={"status": "success"})
