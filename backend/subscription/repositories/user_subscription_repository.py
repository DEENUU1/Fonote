from ..models.user_subscription import UserSubscription
from ..serializers.user_subscription_serializer import UserSubscriptionOutputSerializer
from typing import Dict, Any
from django.contrib.auth.backends import UserModel
from uuid import UUID


class UserSubscriptionRepository:
    def __init__(self):
        self.model = UserSubscription

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscriptionOutputSerializer:
        subscription = self.model.objects.create(
            user=user,
            **data
        )
        return UserSubscriptionOutputSerializer(subscription)

    def get_current_subscription_by_user(self, user: UserModel) -> UserSubscriptionOutputSerializer:
        subscription = self.model.objects.filter(user=user).first()
        return UserSubscriptionOutputSerializer(subscription)

    def change_status(self, _id: UUID, status: str) -> UserSubscriptionOutputSerializer:
        subscription = self.model.objects.get(id=_id)
        subscription.status = status
        subscription.save()
        return UserSubscriptionOutputSerializer(subscription)
