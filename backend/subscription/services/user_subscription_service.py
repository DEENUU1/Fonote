from django.contrib.auth.backends import UserModel

from ..models import UserSubscription
from ..repositories.user_subscription_repository import UserSubscriptionRepository
from typing import Dict, Any
from uuid import UUID
from rest_framework.exceptions import NotFound


class UserSubscriptionService:
    def __init__(self):
        self.user_subscription_repository = UserSubscriptionRepository()

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscription:
        return self.user_subscription_repository.create(data, user)

    def get_current_subscription_by_user(self, user: UserModel) -> UserSubscription:
        return self.user_subscription_repository.get_current_subscription_by_user(user)

    def partial_update(self, user_subscription_id: UUID, data: Dict[str, Any]) -> UserSubscription:
        if not self.user_subscription_repository.user_subscription_exists_by_uuid(user_subscription_id):
            raise NotFound(detail="User subscription not found")

        user_subscription = self.user_subscription_repository.get_user_subscription_by_uuid(user_subscription_id)

        return self.user_subscription_repository.partial_update(user_subscription, data)
