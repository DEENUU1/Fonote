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
    """
    Service class for managing orders.

    Attributes:
        order_repository (OrderRepository): The repository for interacting with orders.
        stripe_service (StripeService): The service for interacting with Stripe.

    Methods:
        create(data: Dict[str, Any], user: UserModel, plan: Plan) -> Order:
            Creates a new order.

        get_order_list_by_user(user_id: int) -> List[Order]:
            Retrieves a list of orders associated with a user.

        get_order_details(uuid: UUID, user_id: int) -> Order:
            Retrieves details of a specific order.

        get_invoice(order_id: UUID, user_id: int) -> str:
            Retrieves the invoice URL for a specific order.
    """

    def __init__(self):
        """
        Initializes the OrderService with necessary repositories and services.
        """
        self.order_repository = OrderRepository()
        self.stripe_service = StripeService()

    def create(self, data: Dict[str, Any], user: UserModel, plan: Plan) -> Order:
        """
        Creates a new order.

        Args:
            data (Dict[str, Any]): The data for creating the order.
            user (UserModel): The user associated with the order.
            plan (Plan): The plan selected for the order.

        Returns:
            Order: The created order.
        """
        return self.order_repository.create(data, user, plan)

    def get_order_list_by_user(self, user_id: int) -> List[Order]:
        """
        Retrieves a list of orders associated with a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[Order]: A list of orders associated with the user.
        """
        return self.order_repository.get_order_list_by_user(user_id)

    def get_order_details(self, uuid: UUID, user_id: int) -> Order:
        """
        Retrieves details of a specific order.

        Args:
            uuid (UUID): The UUID of the order.
            user_id (int): The ID of the user.

        Returns:
            Order: The details of the order.

        Raises:
            PermissionDenied: If the user is not allowed to access the order.
            NotFound: If the order is not found.
        """
        if not self.order_repository.order_object_exists_by_uuid(uuid):
            raise NotFound(detail="Order not found!")

        order = self.order_repository.get_order_object_by_uuid(uuid)

        if not self.order_repository.order_belongs_to_user(order, user_id):
            raise PermissionDenied(detail="You don't have access to this object!")

        return order

    def get_invoice(self, order_id: UUID, user_id: int) -> str:
        """
        Retrieves the invoice URL for a specific order.

        Args:
            order_id (UUID): The UUID of the order.
            user_id (int): The ID of the user.

        Returns:
            str: The URL of the invoice.

        Raises:
            APIException: If the invoice is not found.
        """
        order = self.get_order_details(order_id, user_id)
        invoice_url = self.stripe_service.get_invoice(order.invoice_id)
        if not invoice_url:
            logger.error(f"Invoice not found for order {order_id}")
            raise APIException(f"Invoice not found for order {order_id}")

        return invoice_url


