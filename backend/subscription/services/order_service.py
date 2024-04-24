from typing import Dict, Any, List
from rest_framework.exceptions import PermissionDenied, NotFound, APIException
from django.contrib.auth.backends import UserModel

from uuid import UUID

from ..models import Plan
from ..models.order import Order
from ..repositories.order_repository import OrderRepository
from .stripe_service import StripeService
import logging

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.stripe_service = StripeService()

    def create(self, data: Dict[str, Any], user: UserModel, plan: Plan) -> Order:
        return self.order_repository.create(data, user, plan)

    def get_order_list_by_user(self, user_id: int) -> List[Order]:
        return self.order_repository.get_order_list_by_user(user_id)

    def get_order_details(self, uuid: UUID, user_id: int) -> Order:
        if not self.order_repository.order_object_exists_by_uuid(uuid):
            raise NotFound(detail="Order not found")

        order = self.order_repository.get_order_object_by_uuid(uuid)

        if not self.order_repository.order_belongs_to_user(order, user_id):
            raise PermissionDenied(detail="You are not allowed to access this order")

        return order

    def get_invoice(self, order_id: UUID, user_id: int) -> str:
        order = self.get_order_details(order_id, user_id)
        invoice_url = self.stripe_service.get_invoice(order.invoice_id)
        if not invoice_url:
            logger.error(f"Invoice not found for order {order_id}")
            raise APIException("Invoice not found")

        return invoice_url

