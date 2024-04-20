from .models.input_data import InputData
from rest_framework.serializers import ModelSerializer, DateTimeField


class InputDataInputSerializer(ModelSerializer):
    class Meta:
        model = InputData
        fields = (
            "source_url",
            "language"
        )


class InputDataOutputSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

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
            "language",
            "user",
            "created_at",
            "updated_at"
        )

