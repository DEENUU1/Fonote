from typing import Dict, Any, List

from django.contrib.auth.backends import UserModel

from ..models.order import Order
from ..serializers.order_serializer import OrderInputSerializer
from uuid import UUID


class OrderRepository:
    def __init__(self):
        self.model = Order

    def get_order_object_by_uuid(self, uuid: UUID) -> Order:
        return self.model.objects.get(id=uuid)

    def order_object_exists_by_uuid(self, uuid: UUID) -> bool:
        return self.model.objects.filter(id=uuid).exists()

    def create(self, data: Dict[str, Any], user: UserModel) -> Order:
        return self.model.objects.create(**data, user=user)

    def partial_update(self, data: Dict[str, Any], order: Order) -> Order:
        serializer = OrderInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(order, data)
        return order

    def get_order_list_by_user(self, user_id: int) -> List[Order]:
        return self.model.objects.filter(user_id=user_id)

    def order_belongs_to_user(self, order: Order, user_id: int) -> bool:
        return order.user.id == user_id

