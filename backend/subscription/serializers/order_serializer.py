from rest_framework.serializers import ModelSerializer, DateTimeField

from .plan_serializer import PlanOrderDetailsSerializer
from ..models.order import Order


class OrderInputSerializer(ModelSerializer):
    """
    Serializer for handling input data when creating an order.

    Attributes:
        Meta:
            model (Order): The Order model.
            fields (tuple): The fields to include in the serializer.
    """

    class Meta:
        """
        Metadata class for the OrderInputSerializer.
        """
        model = Order
        fields = (
            "currency",
            "customer",
            "city",
            "country",
            "line1",
            "line2",
            "postal_code",
            "state",
            "email",
            "name",
            "phone",
            "total_amount",
            "invoice_id",
        )


class OrderOutputSerializer(ModelSerializer):
    """
    Serializer for serializing order data for output.

    Attributes:
        created_at (DateTimeField): The field representing the creation date and time.
        updated_at (DateTimeField): The field representing the last update date and time.
        plan (PlanOrderDetailsSerializer): The serializer for including plan details in the output.

    Meta:
        model (Order): The Order model.
        fields (tuple): The fields to include in the serializer.
    """
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    plan = PlanOrderDetailsSerializer(read_only=True)

    class Meta:
        """
        Metadata class for the OrderOutputSerializer.
        """
        model = Order
        fields = (
            "id",
            "user",
            "currency",
            "city",
            "country",
            "line1",
            "line2",
            "postal_code",
            "state",
            "email",
            "phone",
            "total_amount",
            "created_at",
            "updated_at",
            "plan",
        )
