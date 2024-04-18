from rest_framework.serializers import ModelSerializer
from ..models.plan import Plan
from .price_serializer import PriceOutputSerializer


class PlanOutputSerializer(ModelSerializer):
    price = PriceOutputSerializer()

    class Meta:
        model = Plan
        fields = (
            "name",
            "youtube",
            "spotify",
            "ai_transcription",
            "max_length",
            "max_result",
            "duration",
            "price",
        )
