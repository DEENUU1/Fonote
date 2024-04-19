from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.order_serializer import OrderOutputSerializer
from ..services.order_service import OrderService


class OrderDetailsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _order_service = OrderService()

    def get(self, request, pk):
        order = self._order_service.get_order_details(pk, request.user.id)
        return Response(
            OrderOutputSerializer(order).data,
            status=status.HTTP_200_OK
        )
