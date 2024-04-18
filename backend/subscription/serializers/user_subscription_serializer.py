from rest_framework.serializers import ModelSerializer
from ..models.user_subscription import UserSubscription


class UserSubscriptionInputSerializer(ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = (
            "subscription_id",
            "plan",
        )


class UserSubscriptionOutputSerializer(ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = (
            "id",
            "user",
            "subscription_id",
            "plan",
            "start_date",
            "end_date",
            "status"
        )
