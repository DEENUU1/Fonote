from rest_framework.serializers import ModelSerializer, DateTimeField, SerializerMethodField

from ..models.input_data import InputData
from ..serializers.fragment_serializers import FragmentOutputSerializer


class InputDataInputSerializer(ModelSerializer):
    class Meta:
        model = InputData
        fields = (
            "source_url",
            "language",
            "transcription_type"
        )


class InputDataUpdateSerializer(ModelSerializer):
    class Meta:
        model = InputData
        fields = (
            "transcription_type",
            "audio_length",
            "source_title",
        )


class InputDataListOutputSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    audio_length_minutes = SerializerMethodField()

    class Meta:
        model = InputData
        fields = (
            "id",
            "source",
            "transcription_type",
            "audio_length_minutes",
            "source_title",
            "source_url",
            "status",
            "language",
            "user",
            "created_at",
            "updated_at",
        )

    def get_audio_length_minutes(self, obj):
        if not obj.audio_length:
            return None

        return obj.audio_length // 60


class InputDataOutputSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    fragments = FragmentOutputSerializer(many=True, read_only=True)
    audio_length_minutes = SerializerMethodField()

    class Meta:
        model = InputData
        fields = (
            "id",
            "source",
            "transcription_type",
            "audio_length_minutes",
            "source_title",
            "source_url",
            "status",
            "language",
            "user",
            "created_at",
            "updated_at",
            "fragments"
        )

    def get_audio_length_minutes(self, obj):
        if not obj.audio_length:
            return None

        return obj.audio_length // 60
