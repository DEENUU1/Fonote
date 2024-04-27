from rest_framework.serializers import ModelSerializer

from .plan_serializer import PlanOutputSerializer
from ..models.user_subscription import UserSubscription


class UserSubscriptionInputSerializer(ModelSerializer):
    """
    Serializer for handling input data when creating a user subscription.

    Attributes:
        Meta:
            model (UserSubscription): The UserSubscription model.
            fields (tuple): The fields to include in the serializer.
    """

    class Meta:
        """
        Metadata class for the UserSubscriptionInputSerializer.
        """
        model = UserSubscription
        fields = (
            "session_id",
            "plan",
        )


class UserSubscriptionUpdateSerializer(ModelSerializer):
    """
    Serializer for handling input data when updating a user subscription.

    Attributes:
        Meta:
            model (UserSubscription): The UserSubscription model.
            fields (tuple): The fields to include in the serializer.
    """

    class Meta:
        """
        Metadata class for the UserSubscriptionUpdateSerializer.
        """
        model = UserSubscription
        fields = (
            "status",
            "order",
            "subscription_id"
        )


class UserSubscriptionOutputSerializer(ModelSerializer):
    """
    Serializer for serializing user subscription data for output.

    Attributes:
        plan (PlanOutputSerializer): The serializer for including plan details in the output.

    Meta:
        model (UserSubscription): The UserSubscription model.
        fields (tuple): The fields to include in the serializer.
    """
    plan = PlanOutputSerializer()

    class Meta:
        """
        Metadata class for the UserSubscriptionOutputSerializer.
        """
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
    """
    Serializer for serializing detailed user subscription data for output.

    Attributes:
        plan (PlanOutputSerializer): The serializer for including plan details in the output.

    Meta:
        model (UserSubscription): The UserSubscription model.
        fields (tuple): The fields to include in the serializer.
    """
    plan = PlanOutputSerializer()

    class Meta:
        """
        Metadata class for the UserSubscriptionDetailOutputSerializer.
        """
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
