import logging
from datetime import date
from typing import Dict, Any
from uuid import UUID

from django.contrib.auth.backends import UserModel
from rest_framework.exceptions import NotFound, APIException, PermissionDenied

from .stripe_service import StripeService
from ..models import UserSubscription
from ..repositories.user_subscription_repository import UserSubscriptionRepository
from ..services.plan_service import PlanService

logger = logging.getLogger(__name__)


class UserSubscriptionService:
    """
    Service class for managing user subscriptions.

    Attributes:
        None

    Methods:
        create(data: Dict[str, Any], user: UserModel) -> UserSubscription:
            Creates a new user subscription.

        get_current_subscription_by_user(user: UserModel) -> UserSubscription:
            Retrieves the current subscription of a user.

        partial_update(user_subscription_id: UUID, data: Dict[str, Any]) -> UserSubscription:
            Updates a user subscription with partial data.

        subscription_is_valid(user_subscription: UserSubscription) -> bool:
            Checks if a user subscription is currently valid.

        create_checkout_session(user: UserModel, plan_id) -> str:
            Creates a checkout session for subscribing to a plan.

        cancel_subscription(user: UserModel) -> None:
            Cancels the current subscription of a user.
    """

    def __init__(self):
        """
        Initializes the UserSubscriptionService with necessary dependencies.
        """
        self.user_subscription_repository = UserSubscriptionRepository()
        self.stripe_service = StripeService()
        self.plan_service = PlanService()

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscription:
        """
        Creates a new user subscription.

        Args:
            data (Dict[str, Any]): Data for creating the subscription.
            user (UserModel): The user for whom the subscription is created.

        Returns:
            UserSubscription: The created user subscription.
        """
        return self.user_subscription_repository.create(data, user)

    def get_current_subscription_by_user(self, user: UserModel) -> UserSubscription:
        """
        Retrieves the current subscription of a user.

        Args:
            user (UserModel): The user whose subscription is to be retrieved.

        Returns:
            UserSubscription: The current user subscription.
        """
        return self.user_subscription_repository.get_current_subscription_by_user(user)

    def partial_update(self, user_subscription_id: UUID, data: Dict[str, Any]) -> UserSubscription:
        """
        Updates a user subscription with partial data.

        Args:
            user_subscription_id (UUID): The ID of the user subscription to be updated.
            data (Dict[str, Any]): Partial data to update the user subscription.

        Returns:
            UserSubscription: The updated user subscription.
        """
        if not self.user_subscription_repository.user_subscription_exists_by_uuid(user_subscription_id):
            raise NotFound(detail="User subscription not found")

        user_subscription = self.user_subscription_repository.get_user_subscription_by_uuid(user_subscription_id)

        return self.user_subscription_repository.partial_update(user_subscription, data)

    @staticmethod
    def subscription_is_valid(user_subscription: UserSubscription) -> bool:
        """
        Checks if a user subscription is currently valid.

        Args:
            user_subscription (UserSubscription): The user subscription to be checked.

        Returns:
            bool: True if the subscription is valid, False otherwise.
        """
        today = date.today()

        if user_subscription.start_date or user_subscription.end_date is None:
            return False

        if user_subscription.start_date >= today or user_subscription.end_date <= today:
            return False

        return True

    def create_checkout_session(self, user: UserModel, plan_id) -> str:
        """
        Creates a checkout session for subscribing to a plan.

        Args:
            user (UserModel): The user initiating the checkout.
            plan_id: The ID of the plan to subscribe to.

        Returns:
            str: The URL of the created checkout session.
        """
        user_current_plan = self.user_subscription_repository.get_current_subscription_by_user(user)

        if user_current_plan:
            if user_current_plan.status == "ACTIVE" or self.subscription_is_valid(user_current_plan):
                raise PermissionDenied(detail="You already have an active subscription")

        plan = self.plan_service.get_plan_by_id(plan_id)
        checkout_session = self.stripe_service.create_checkout_session(plan.price.stripe_id, user.id, plan.pk)
        if not checkout_session:
            logger.error("Error creating checkout session")
            raise APIException(detail="Error creating checkout session")

        self.user_subscription_repository.create({"session_id": checkout_session.id, "plan": plan}, user)
        return checkout_session.url

    def cancel_subscription(self, user: UserModel) -> None:
        """
        Cancels the current subscription of a user.

        Args:
            user (UserModel): The user whose subscription is to be canceled.

        Returns:
            None
        """
        user_current_plan = self.user_subscription_repository.get_current_subscription_by_user(user)

        if not user_current_plan:
            raise NotFound(detail="You don't have an active subscription")

        if user_current_plan and user_current_plan.status == "CANCELED":
            raise APIException(detail="You already canceled your subscription")

        if user_current_plan and user_current_plan.status != "ACTIVE":
            raise APIException(detail="You don't have an active subscription")

        cancelled_subscription = self.stripe_service.cancel_subscription(user_current_plan.subscription_id)
        if not cancelled_subscription:
            logger.error("Error canceling subscription")
            raise APIException(detail="Error canceling subscription")

        self.user_subscription_repository.partial_update(user_current_plan, {"status": "CANCELED"})
        logger.info(
            f"Subscription canceled successfully user: {user} subscription: {user_current_plan.subscription_id}"
        )
        return
