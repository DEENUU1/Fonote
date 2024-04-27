from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user_subscription_serializer import UserSubscriptionOutputSerializer
from ..services.user_subscription_service import UserSubscriptionService


class UserSubscriptionAPIView(APIView):
    """
    API endpoint to retrieve the current subscription details for the authenticated user.
    """

    permission_classes = (IsAuthenticated,)
    _service = UserSubscriptionService()

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        """
        Retrieve the current subscription details for the authenticated user.

        Parameters:
        - request: HTTP request object.

        Returns:
        - Response: HTTP response containing the serialized subscription data.
        """
        user_subscription = self._service.get_current_subscription_by_user(request.user)
        return Response(UserSubscriptionOutputSerializer(user_subscription).data, status=status.HTTP_200_OK)
