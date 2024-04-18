from django.contrib.auth.backends import UserModel

from ..repositories.user_subscription_repository import UserSubscriptionRepository
from ..serializers.user_subscription_serializer import UserSubscriptionOutputSerializer
from typing import Dict, Any
from uuid import UUID


class UserSubscriptionService:
    def __init__(self):
        self.user_subscription_repository = UserSubscriptionRepository()

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscriptionOutputSerializer:
        return self.user_subscription_repository.create(data, user)

    def get_current_subscription_by_user(self, user: UserModel) -> UserSubscriptionOutputSerializer:
        return self.user_subscription_repository.get_current_subscription_by_user(user)

    def change_status(self, _id: UUID, status: str) -> UserSubscriptionOutputSerializer:
        return self.user_subscription_repository.change_status(_id, status)



