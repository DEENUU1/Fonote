from typing import Dict, Any, Optional, List

from django.contrib.auth.backends import UserModel

from uuid import UUID

from ..models.order import Order
from ..repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()

    def create(self, data: Dict[str, Any], user: UserModel) -> Order:
        return self.order_repository.create(data, user)

    def partial_update_by_uuid(self, data: Dict[str, Any], uuid: UUID) -> Optional[Order]:
        if not self.order_repository.order_object_exists_by_uuid(uuid):
            return None

        order = self.order_repository.get_order_object_by_uuid(uuid)
        return self.order_repository.partial_update(data, order)

    def partial_update_by_invoice_id(self, data: Dict[str, Any], invoice_id: str) -> Optional[Order]:
        if not self.order_repository.order_exists_by_invoice_id(invoice_id):
            return None

        order = self.order_repository.get_order_by_invoice_id(invoice_id)
        return self.order_repository.partial_update(data, order)

    def get_order_list_by_user(self, user_id: int) -> List[Order]:
        return self.order_repository.get_order_list_by_user(user_id)

    def get_order_details(self, uuid: UUID, user_id: int) -> Optional[Order]:
        if not self.order_repository.order_object_exists_by_uuid(uuid):
            return None

        order = self.order_repository.get_order_object_by_uuid(uuid)

        if not self.order_repository.order_belongs_to_user(order, user_id):
            return None

        return order
