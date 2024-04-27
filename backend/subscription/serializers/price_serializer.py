from rest_framework.serializers import ModelSerializer

from ..models.price import Price


class PriceOutputSerializer(ModelSerializer):
    """
    Serializer for serializing price data for output.

    Meta:
        model (Price): The Price model.
        fields (tuple): The fields to include in the serializer.
    """

    class Meta:
        """
        Metadata class for the PriceOutputSerializer.
        """
        model = Price
        fields = (
            "price",
            "prev_price"
        )
