from rest_framework.serializers import ModelSerializer

from ..models.price import Price


class PriceOutputSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = (
            "price",
            "prev_price"
        )
