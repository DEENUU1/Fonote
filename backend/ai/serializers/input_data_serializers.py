from rest_framework.serializers import ModelSerializer, DateTimeField, SerializerMethodField

from ..models.input_data import InputData
from ..serializers.fragment_serializers import FragmentOutputSerializer
from rest_framework.exceptions import ValidationError


class InputDataInputSerializer(ModelSerializer):
    """Serializer for input data input."""

    class Meta:
        """Metadata options for the InputDataInputSerializer."""

        model = InputData
        fields = (
            "source_url",
            "language",
            "transcription_type"
        )

    def validate_transcription_type(self, value: str) -> str:
        """
        Validates the transcription type.

        Parameters:
        value (str): The transcription type to be validated.

        Returns:
        str: The validated transcription type.

        Raises:
        ValidationError: If the provided value is not one of ["GENERATED", "MANUAL", "LLM"].
        """

        if value not in ["GENERATED", "MANUAL", "LLM"]:
            raise ValidationError("Invalid transcription type")
        return value

    def validate_source_url(self, value: str) -> str:
        """
        Validates the source URL.

        Parameters:
        value (str): The URL to be validated.

        Returns:
        str: The validated URL.

        Raises:
        ValidationError: If the provided URL does not contain "youtube.com/" or "spotify.com/".
        """

        if "youtube.com/" not in value and "spotify.com/" not in value:
            raise ValidationError("Invalid url")
        return value


class InputDataUpdateSerializer(ModelSerializer):
    """Serializer for updating input data."""

    class Meta:
        """Metadata options for the InputDataUpdateSerializer."""

        model = InputData
        fields = (
            "transcription_type",
            "audio_length",
            "source_title",
        )


class InputDataListOutputSerializer(ModelSerializer):
    """Serializer for listing output data of input data."""

    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    audio_length_minutes = SerializerMethodField()

    class Meta:
        """Metadata options for the InputDataListOutputSerializer."""

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
        """Retrieve audio length in minutes.

        Args:
            obj: The instance of the model.

        Returns:
            int: Audio length in minutes.
        """
        if not obj.audio_length:
            return None

        return obj.audio_length // 60


class InputDataOutputSerializer(ModelSerializer):
    """Serializer for output data of input data."""

    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    fragments = FragmentOutputSerializer(many=True, read_only=True)
    audio_length_minutes = SerializerMethodField()

    class Meta:
        """Metadata options for the InputDataOutputSerializer."""

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
        """Retrieve audio length in minutes.

        Args:
            obj: The instance of the model.

        Returns:
            int: Audio length in minutes.
        """
        if not obj.audio_length:
            return None

        return obj.audio_length // 60
