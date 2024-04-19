from ..models.user_subscription import UserSubscription
from typing import Dict, Any, Optional
from django.contrib.auth.backends import UserModel
from uuid import UUID


class UserSubscriptionRepository:
    def __init__(self):
        self.model = UserSubscription

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscription:
        return self.model.objects.create(user=user, **data)

    @staticmethod
    def partial_update(user_subscription: UserSubscription, data: Dict[str, Any]) -> UserSubscription:
        for key, value in data.items():
            setattr(user_subscription, key, value)
        user_subscription.save()
        return user_subscription

    def user_subscription_exists_by_uuid(self, _id: UUID) -> bool:
        return self.model.objects.filter(id=_id).exists()

    def get_user_subscription_by_uuid(self, _id: UUID) -> UserSubscription:
        return self.model.objects.get(id=_id)

    def get_current_subscription_by_user(self, user: UserModel) -> Optional[UserSubscription]:
        return self.model.objects.filter(user=user).first()

