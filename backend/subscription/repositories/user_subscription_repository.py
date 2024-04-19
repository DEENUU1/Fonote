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
        return UserSubscriptionOutputSerializer(subscription).data

    def change_status(self, _id: UUID, status: str) -> UserSubscriptionOutputSerializer:
        subscription = self.model.objects.get(id=_id)
        subscription.status = status
        subscription.save()
        return UserSubscriptionOutputSerializer(subscription)

    def get_by_subscription_id(self, subscription_id: str) -> UserSubscriptionOutputSerializer:
        subscription = self.model.objects.get(subscription_id=subscription_id)
        return UserSubscriptionOutputSerializer(subscription)

    def user_subscription_exists_by_subscription_id(self, subscription_id: str) -> bool:
        return self.model.objects.filter(subscription_id=subscription_id).exists()

    def get_by_session_id(self, session_id: str) -> UserSubscriptionOutputSerializer:
        subscription = self.model.objects.get(session_id=session_id)
        return UserSubscriptionOutputSerializer(subscription)

    def user_subscription_exists_by_session_id(self, session_id: str) -> bool:
        return self.model.objects.filter(session_id=session_id).exists()
