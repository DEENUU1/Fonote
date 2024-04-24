from rest_framework.serializers import ModelSerializer
from ..models.user_subscription import UserSubscription
from .plan_serializer import PlanOutputSerializer


class UserSubscriptionInputSerializer(ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = (
            "session_id",
            "plan",
        )


class UserSubscriptionUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = (
            "status",
            "order",
            "subscription_id"
        )


class UserSubscriptionOutputSerializer(ModelSerializer):
    plan = PlanOutputSerializer()

    class Meta:
        model = UserSubscription
        fields = (
            "id",
            "user",
            "session_id",
            "subscription_id",
            "plan",
            "start_date",
            "end_date",
            "status",
            "order"
        )


class UserSubscriptionDetailOutputSerializer(ModelSerializer):
    plan = PlanOutputSerializer()

    class Meta:
        model = UserSubscription
        fields = (
            "id",
            "user",
            "subscription_id",
            "plan",
            "start_date",
            "end_date",
            "status",
            "order"
        )
