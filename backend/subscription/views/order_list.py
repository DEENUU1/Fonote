from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.order_serializer import OrderOutputSerializer
from ..services.order_service import OrderService


class OrderListAPIView(APIView):
    """
    API view for retrieving a list of orders belonging to the authenticated user.

    Attributes:
        permission_classes (tuple): Tuple containing IsAuthenticated permission class.
        _order_service (OrderService): Instance of OrderService for handling order-related operations.

    Methods:
        get(request) -> Response:
            Retrieves a list of orders for the authenticated user.
    """

    permission_classes = (IsAuthenticated,)
    _order_service = OrderService()

    def get(self, request):
        """
        Retrieves a list of orders for the authenticated user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: Response containing the list of orders belonging to the authenticated user.
        """
        orders = self._order_service.get_order_list_by_user(request.user)
        return Response(
            OrderOutputSerializer(orders, many=True).data,
            status=status.HTTP_200_OK
        )
