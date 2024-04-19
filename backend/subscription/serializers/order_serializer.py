from rest_framework.serializers import ModelSerializer, DateTimeField
from ..models.order import Order


class OrderInputSerializer(ModelSerializer):
    class Meta:
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
            "stripe_id",
            "total_amount",
            "invoice_url",
            "invoice_id",
        )


class OrderOutputSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
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
            "invoice_url"
        )
