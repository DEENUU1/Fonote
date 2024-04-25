from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.user_subscription_service import UserSubscriptionService


class CreateSubscription(APIView):
    permission_classes = (IsAuthenticated,)
    _service = UserSubscriptionService()

    def post(self, request):
        checkout_session_url = self._service.create_checkout_session(request.user, request.data.get("plan_id"))
        return Response(data=checkout_session_url, status=status.HTTP_200_OK)
