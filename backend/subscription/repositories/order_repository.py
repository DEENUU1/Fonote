from typing import Dict, Any, List
from uuid import UUID

from django.contrib.auth.backends import UserModel

from ..models import Plan
from ..models.order import Order


class OrderRepository:
    """
    Repository for interacting with order data.

    Methods:
        get_order_object_by_uuid(uuid: UUID) -> Order:
            Retrieves an order by its UUID.

        order_object_exists_by_uuid(uuid: UUID) -> bool:
            Checks if an order with the given UUID exists.

        create(data: Dict[str, Any], user: UserModel, plan: Plan) -> Order:
            Creates a new order with the given data, user, and plan.

        get_order_list_by_user(user_id: int) -> List[Order]:
            Retrieves a list of orders associated with a user.

        order_belongs_to_user(order: Order, user_id: int) -> bool:
            Checks if the given order belongs to the specified user.

    Attributes:
        model: The Order model used for database operations.
    """

    def __init__(self):
        """
        Initialize the OrderRepository.
        """
        self.model = Order

    def get_order_object_by_uuid(self, uuid: UUID) -> Order:
        """
        Retrieves an order by its UUID.

        Args:
            uuid (UUID): The UUID of the order.

        Returns:
            Order: The order object.
        """
        return self.model.objects.get(id=uuid)

    def order_object_exists_by_uuid(self, uuid: UUID) -> bool:
        """
        Checks if an order with the given UUID exists.

        Args:
            uuid (UUID): The UUID of the order.

        Returns:
            bool: True if the order exists, False otherwise.
        """
        return self.model.objects.filter(id=uuid).exists()

    def create(self, data: Dict[str, Any], user: UserModel, plan: Plan) -> Order:
        """
        Creates a new order with the given data, user, and plan.

        Args:
            data (Dict[str, Any]): The data to create the order with.
            user (UserModel): The user associated with the order.
            plan (Plan): The plan associated with the order.

        Returns:
            Order: The created order object.
        """
        return self.model.objects.create(**data, user=user, plan=plan)

    def get_order_list_by_user(self, user_id: int) -> List[Order]:
        """
        Retrieves a list of orders associated with a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[Order]: A list of orders associated with the user.
        """
        return self.model.objects.filter(user_id=user_id)

    @staticmethod
    def order_belongs_to_user(order: Order, user_id: int) -> bool:
        """
        Checks if the given order belongs to the specified user.

        Args:
            order (Order): The order object.
            user_id (int): The ID of the user.

        Returns:
            bool: True if the order belongs to the user, False otherwise.
        """
        return order.user.id == user_id
