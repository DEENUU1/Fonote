from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.user_subscription_service import UserSubscriptionService


class CancelSubscription(APIView):
    permission_classes = (IsAuthenticated,)
    _user_service = UserSubscriptionService()

    def post(self, request):
        self._user_service.cancel_subscription(request.user)
        return Response(
            {"message": "Subscription canceled successfully"},
            status=status.HTTP_200_OK
        )
