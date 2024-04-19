from ..models.order import Order
from ..models.user_subscription import UserSubscription
from typing import Dict, Any
from django.contrib.auth.backends import UserModel
from uuid import UUID


class UserSubscriptionRepository:
    def __init__(self):
        self.model = UserSubscription

    def create(self, data: Dict[str, Any], user: UserModel) -> UserSubscription:
        return self.model.objects.create(user=user, **data)

    def get_current_subscription_by_user(self, user: UserModel) -> UserSubscription:
        return self.model.objects.filter(user=user).first()

    def change_status(self, subscription: UserSubscription, status: str) -> UserSubscription:
        subscription.status = status
        subscription.save()
        return subscription

    def get_by_subscription_id(self, subscription_id: str) -> UserSubscription:
        return self.model.objects.get(subscription_id=subscription_id)

    def user_subscription_exists_by_subscription_id(self, subscription_id: str) -> bool:
        return self.model.objects.filter(subscription_id=subscription_id).exists()

    def get_by_session_id(self, session_id: str) -> UserSubscription:
        return self.model.objects.get(session_id=session_id)

    def user_subscription_exists_by_session_id(self, session_id: str) -> bool:
        return self.model.objects.filter(session_id=session_id).exists()

    def user_subscription_exists_by_uuid(self, _id: UUID) -> bool:
        return self.model.objects.filter(id=_id).exists()

    def get_user_subscription_by_uuid(self, _id: UUID) -> UserSubscription:
        return self.model.objects.get(id=_id)

    def set_order_object(self, subscription: UserSubscription, order: Order) -> None:
        subscription.order = order
        subscription.save()
        return

