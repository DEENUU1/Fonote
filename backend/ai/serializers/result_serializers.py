from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, DateTimeField

from ..models.result import Result


class ResultInputSerializer(ModelSerializer):
    """Serializer for result input data."""

    input_id = serializers.UUIDField()

    class Meta:
        """Metadata options for the ResultInputSerializer."""

        model = Result
        fields = (
            "result_type",
            "input_id"
        )


class ResultOutputSerializer(ModelSerializer):
    """Serializer for output data of result."""

    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metadata options for the ResultOutputSerializer."""

        model = Result
        fields = (
            "id",
            "content",
            "result_type",
            "input",
            "created_at",
            "updated_at"
        )
