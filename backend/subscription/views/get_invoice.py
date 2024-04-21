from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.order_service import OrderService


class GetInvoice(APIView):
    permission_classes = (IsAuthenticated,)
    _order_service = OrderService()

    def get(self, request, pk):
        invoice_url = self._order_service.get_invoice(pk, request.user.id)
        return Response({"message": invoice_url}, status=status.HTTP_200_OK)
