from rest_framework.serializers import ModelSerializer

from .price_serializer import PriceOutputSerializer
from ..models.plan import Plan


class PlanOutputSerializer(ModelSerializer):
    price = PriceOutputSerializer()

    class Meta:
        model = Plan
        fields = (
            "id",
            "name",
            "youtube",
            "spotify",
            "max_length",
            "max_result",
            "duration",
            "price",
        )
