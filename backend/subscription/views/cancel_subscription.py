import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user_subscription_serializer import UserSubscriptionUpdateSerializer
from ..services.user_subscription_service import UserSubscriptionService

stripe.api_key = settings.STRIPE_SECRET_KEY


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

        return Response({"message": "Subscription canceled successfully"}, status=status.HTTP_200_OK)
