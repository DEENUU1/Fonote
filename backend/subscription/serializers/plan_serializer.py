from rest_framework.serializers import ModelSerializer, DateTimeField
from ..models.plan import Plan


class PlanOutputSerializer(ModelSerializer):
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
