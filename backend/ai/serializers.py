from .models import InputData
from rest_framework.serializers import ModelSerializer


class InputDataInputSerializer(ModelSerializer):
    class Meta:
        model = InputData
        fields = (
            "source",
            "source_url",
        )


class InputDataOutputSerializer(ModelSerializer):
    class Meta:
        model = InputData
        fields = (
            "id",
            "source",
            "transcription_type",
            "audio_length",
            "source_title",
            "source_url",
            "status",
            "user"  # TODO change this later
        )
