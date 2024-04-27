from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.order_service import OrderService


class GetInvoice(APIView):
    """
    API view for retrieving the invoice URL of a user's order.

    Attributes:
        permission_classes (tuple): Tuple containing IsAuthenticated permission class.
        _order_service (OrderService): Instance of OrderService for handling order-related operations.

    Methods:
        get(request, pk) -> Response:
            Retrieves the invoice URL of the specified order for the authenticated user.
    """

    permission_classes = (IsAuthenticated,)
    _order_service = OrderService()

    def get(self, request, pk):
        """
        Retrieves the invoice URL of the specified order for the authenticated user.

        Args:
            request (Request): The HTTP request object.
            pk (str): The UUID of the order to retrieve the invoice URL for.

        Returns:
            Response: Response containing the invoice URL of the specified order.
        """
        invoice_url = self._order_service.get_invoice(pk, request.user.id)
        return Response({"message": invoice_url}, status=status.HTTP_200_OK)
