from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.user_subscription_service import UserSubscriptionService


class CancelSubscription(APIView):
    """
    API view for canceling a user's subscription.

    Attributes:
        permission_classes (tuple): Tuple containing IsAuthenticated permission class.

    Methods:
        post(request) -> Response:
            Cancels the subscription of the authenticated user.
    """

    permission_classes = (IsAuthenticated,)
    _user_service = UserSubscriptionService()

    def post(self, request):
        """
        Cancels the subscription of the authenticated user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: Response indicating the success of the operation.
        """
        self._user_service.cancel_subscription(request.user)
        return Response(
            {"message": "Subscription canceled successfully"},
            status=status.HTTP_200_OK
        )
