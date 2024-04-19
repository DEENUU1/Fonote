from typing import Dict, Any

from django.contrib.auth.backends import UserModel

from ..models.order import Order
from ..serializers.order_serializer import OrderOutputSerializer, OrderInputSerializer
from uuid import UUID


class OrderRepository:
    def __init__(self):
        self.model = Order

    def get_order_object_by_uuid(self, uuid: UUID):
        return self.model.objects.get(uuid=uuid)

    def order_object_exists_by_uuid(self, uuid: UUID) -> bool:
        return self.model.objects.filter(uuid=uuid).exists()

    def create(self, data: Dict[str, Any], user: UserModel):
        order_db = self.model.objects.create(**data, user=user)
        return OrderOutputSerializer(order_db).data

    def partial_update(self, data: Dict[str, Any], order: Order):
        serializer = OrderInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(order, data)
        return OrderOutputSerializer(order).data

    def get_order_by_invoice_id(self, invoice_id: str) -> Order:
        return self.model.objects.get(invoice_id=invoice_id)

    def order_exists_by_invoice_id(self, invoice_id: str) -> bool:
        return self.model.objects.filter(invoice_id=invoice_id).exists()
