from django.contrib.auth.backends import UserModel

from ..models import UserSubscription
from ..models.order import Order
from ..repositories.user_subscription_repository import UserSubscriptionRepository
from typing import Dict, Any, Optional
from uuid import UUID


class UserSubscriptionService:
    def __init__(self):
        self.user_subscription_repository = UserSubscriptionRepository()

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscription:
        return self.user_subscription_repository.create(data, user)

    def get_current_subscription_by_user(self, user: UserModel) -> UserSubscription:
        return self.user_subscription_repository.get_current_subscription_by_user(user)

    def change_status(self, _id: UUID, status: str) -> Optional[UserSubscription]:
        if not self.user_subscription_repository.user_subscription_exists_by_uuid(_id):
            return None

        user_subscription = self.user_subscription_repository.get_user_subscription_by_uuid(_id)

        return self.user_subscription_repository.change_status(user_subscription, status)

    def set_order_object(self, _id: UUID, order: Order) -> None:
        if not self.user_subscription_repository.user_subscription_exists_by_uuid(_id):
            return None

        user_subscription = self.user_subscription_repository.get_user_subscription_by_uuid(_id)

        return self.user_subscription_repository.set_order_object(user_subscription, order)

    def set_subscription_id(self, _id: UUID, subscription_id: str) -> None:
        if not self.user_subscription_repository.user_subscription_exists_by_uuid(_id):
            return None

        user_subscription = self.user_subscription_repository.get_user_subscription_by_uuid(_id)

        return self.user_subscription_repository.set_subscription_id(user_subscription, subscription_id)

    def get_by_subscription_id(self, subscription_id: str) -> Optional[UserSubscription]:
        if not self.user_subscription_repository.user_subscription_exists_by_subscription_id(subscription_id):
            return None

        return self.user_subscription_repository.get_by_subscription_id(subscription_id)

    def get_by_session_id(self, session_id: str) -> Optional[UserSubscription]:
        if not self.user_subscription_repository.user_subscription_exists_by_session_id(session_id):
            return None

        return self.user_subscription_repository.get_by_session_id(session_id)
