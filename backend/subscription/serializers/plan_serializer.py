from rest_framework.serializers import ModelSerializer

from .price_serializer import PriceOutputSerializer
from ..models.plan import Plan


class PlanOutputSerializer(ModelSerializer):
    """
    Serializer for serializing plan data for output.

    Attributes:
        price (PriceOutputSerializer): The serializer for including price details in the output.

    Meta:
        model (Plan): The Plan model.
        fields (tuple): The fields to include in the serializer.
    """
    price = PriceOutputSerializer()

    class Meta:
        """
        Metadata class for the PlanOutputSerializer.
        """
        model = Plan
        fields = (
            "id",
            "name",
            "description",
            "youtube",
            "spotify",
            "max_result",
            "duration",
            "price",
            "change_lang",
            "ai_transcription",
        )


class PlanOrderDetailsSerializer(ModelSerializer):
    """
    Serializer for including minimal plan details in order-related output.

    Meta:
        model (Plan): The Plan model.
        fields (tuple): The fields to include in the serializer.
    """

    class Meta:
        """
        Metadata class for the PlanOrderDetailsSerializer.
        """
        model = Plan
        fields = (
            "id",
            "name",
        )
