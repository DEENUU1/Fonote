from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.order_serializer import OrderOutputSerializer
from ..services.order_service import OrderService


class OrderDetailsAPIView(APIView):
    """
    API view for retrieving details of a specific order belonging to the authenticated user.

    Attributes:
        permission_classes (tuple): Tuple containing IsAuthenticated permission class.
        _order_service (OrderService): Instance of OrderService for handling order-related operations.

    Methods:
        get(request, pk) -> Response:
            Retrieves details of the specified order for the authenticated user.
    """

    permission_classes = (IsAuthenticated,)
    _order_service = OrderService()

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, pk):
        """
        Retrieves details of the specified order for the authenticated user.

        Args:
            request (Request): The HTTP request object.
            pk (str): The UUID of the order to retrieve details for.

        Returns:
            Response: Response containing the details of the specified order.
        """
        order = self._order_service.get_order_details(pk, request.user.id)
        return Response(
            OrderOutputSerializer(order).data,
            status=status.HTTP_200_OK
        )
