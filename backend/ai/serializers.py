from .models.input_data import InputData
from rest_framework.serializers import ModelSerializer, DateTimeField
from .models.fragment import Fragment


class FragmentInputSerializer(ModelSerializer):
    class Meta:
        model = Fragment
        fields = (
            "start_time",
            "end_time",
            "order",
            "text",
            "input_data"
        )


class FragmentOutputSerializer(ModelSerializer):
    class Meta:
        model = Fragment
        fields = (
            "id",
            "start_time",
            "end_time",
            "order",
            "text",
            "input_data"
        )


class InputDataInputSerializer(ModelSerializer):
    class Meta:
        model = InputData
        fields = (
            "source_url",
            "language"
        )


class InputDataListOutputSerializer(ModelSerializer):
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
            "updated_at",
        )


class InputDataOutputSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    fragments = FragmentOutputSerializer(many=True, read_only=True)

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
            "updated_at",
            "fragments"
        )
