from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.user_subscription_service import UserSubscriptionService


class CreateSubscription(APIView):
    """
    API view for creating a new subscription for the authenticated user.

    Attributes:
        permission_classes (tuple): Tuple containing IsAuthenticated permission class.
        _service (UserSubscriptionService): Instance of UserSubscriptionService for handling subscription creation.

    Methods:
        post(request) -> Response:
            Creates a new subscription for the authenticated user based on the provided plan ID.
    """

    permission_classes = (IsAuthenticated,)
    _service = UserSubscriptionService()

    def post(self, request):
        """
        Creates a new subscription for the authenticated user based on the provided plan ID.

        Args:
            request (Request): The HTTP request object containing the plan ID in the data.

        Returns:
            Response: Response containing the URL of the checkout session for the new subscription.
        """
        checkout_session_url = self._service.create_checkout_session(request.user, request.data.get("plan_id"))
        return Response(data=checkout_session_url, status=status.HTTP_200_OK)
