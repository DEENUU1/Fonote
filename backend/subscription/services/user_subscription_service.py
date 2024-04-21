from django.contrib.auth.backends import UserModel

from ..models import UserSubscription
from ..repositories.user_subscription_repository import UserSubscriptionRepository
from typing import Dict, Any
from uuid import UUID
from rest_framework.exceptions import NotFound, ValidationError, APIException
from datetime import date
from .stripe_service import StripeService
from ..services.plan_service import PlanService
import logging


logger = logging.getLogger(__name__)


class UserSubscriptionService:
    def __init__(self):
        self.user_subscription_repository = UserSubscriptionRepository()
        self.stripe_service = StripeService()
        self.plan_service = PlanService()

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscription:
        return self.user_subscription_repository.create(data, user)

    def get_current_subscription_by_user(self, user: UserModel) -> UserSubscription:
        return self.user_subscription_repository.get_current_subscription_by_user(user)

    def partial_update(self, user_subscription_id: UUID, data: Dict[str, Any]) -> UserSubscription:
        if not self.user_subscription_repository.user_subscription_exists_by_uuid(user_subscription_id):
            raise NotFound(detail="User subscription not found")

        user_subscription = self.user_subscription_repository.get_user_subscription_by_uuid(user_subscription_id)

        return self.user_subscription_repository.partial_update(user_subscription, data)

    @staticmethod
    def subscription_is_valid(user_subscription: UserSubscription) -> bool:
        today = date.today()

        if user_subscription.start_date or user_subscription.end_date is None:
            return False

        if user_subscription.start_date >= today or user_subscription.end_date <= today:
            return False

        return True

    def create_checkout_session(self, user: UserModel, price_id) -> str:
        user_current_plan = self.user_subscription_repository.get_current_subscription_by_user(user)

        if user_current_plan:
            if user_current_plan.status == "ACTIVE" or self.subscription_is_valid(user_current_plan):
                raise ValidationError(detail="You already have an active subscription")

        checkout_session = self.stripe_service.create_checkout_session(price_id, user.id)
        if not checkout_session:
            logger.error("Error creating checkout session")
            raise APIException(detail="Error creating checkout session")

        plan = self.plan_service.get_plan_by_price_id(price_id)
        self.user_subscription_repository.create({"session_id": checkout_session.id, "plan": plan.pk}, user)
        return checkout_session.url

    def cancel_subscription(self, user: UserModel) -> None:
        user_current_plan = self.user_subscription_repository.get_current_subscription_by_user(user)

        if not user_current_plan:
            raise ValidationError(detail="You don't have an active subscription")

        if user_current_plan and user_current_plan.status == "CANCELED":
            raise ValidationError(detail="You already canceled your subscription")

        if user_current_plan and user_current_plan.status != "ACTIVE":
            raise ValidationError(detail="You don't have an active subscription")

        cancelled_subscription = self.stripe_service.cancel_subscription(user_current_plan.subscription_id)
        if not cancelled_subscription:
            logger.error("Error canceling subscription")
            raise APIException(detail="Error canceling subscription")

        self.user_subscription_repository.partial_update(user_current_plan, {"status": "CANCELED"})
        logger.info(
            f"Subscription canceled successfully user: {user} subscription: {user_current_plan.subscription_id}"
        )
        return
