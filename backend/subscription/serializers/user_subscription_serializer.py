from rest_framework.serializers import ModelSerializer
from ..models.user_subscription import UserSubscription
from .plan_serializer import PlanOutputSerializer


class UserSubscriptionInputSerializer(ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = (
            # "subscription_id",
            "session_id",
            "plan",
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
            "status"
        )
