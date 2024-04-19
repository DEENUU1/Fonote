from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.order_serializer import OrderOutputSerializer
from ..services.order_service import OrderService


class OrderListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _order_service = OrderService()

    def get(self, request):
        orders = self._order_service.get_order_list_by_user(request.user)
        return Response(
            OrderOutputSerializer(orders, many=True).data,
            status=status.HTTP_200_OK
        )
