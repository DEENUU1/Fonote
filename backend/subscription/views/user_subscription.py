from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.user_subscription_service import UserSubscriptionService
from ..serializers.user_subscription_serializer import UserSubscriptionOutputSerializer


class UserSubscriptionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _service = UserSubscriptionService()

    def get(self, request):
        user_subscription = self._service.get_current_subscription_by_user(request.user)
        return Response(UserSubscriptionOutputSerializer(user_subscription).data, status=status.HTTP_200_OK)
