import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.order_service import OrderService

stripe.api_key = settings.STRIPE_SECRET_KEY


class GetInvoice(APIView):
    permission_classes = (IsAuthenticated,)
    _order_service = OrderService()

    def get(self, request, pk):
        order = self._order_service.get_order_details(pk, request.user.id)

        try:
            invoice_data = stripe.Invoice.retrieve(order.invoice_id)
            return Response(
                {"message": invoice_data.hosted_invoice_url},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            raise e
