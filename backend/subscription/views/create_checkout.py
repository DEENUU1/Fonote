import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user_subscription_serializer import UserSubscriptionInputSerializer
from ..services.plan_service import PlanService
from ..services.user_subscription_service import UserSubscriptionService

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateSubscription(APIView):
    permission_classes = (IsAuthenticated,)

    _service = UserSubscriptionService()
    _plan_service = PlanService()

    def post(self, request):
        user_current_plan = self._service.get_current_subscription_by_user(request.user)

        if user_current_plan:
            if user_current_plan.status == "ACTIVE" or self._service.subscription_is_valid(user_current_plan):
                return Response(
                    {"message": "You already have an active subscription"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': request.data['price_id'],
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

            # Get Plan object by price_id
            plan = self._plan_service.get_plan_by_price_id(request.data["price_id"])

            # Create UserSubscription object
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
