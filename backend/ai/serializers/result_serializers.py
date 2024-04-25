from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, DateTimeField

from ..models.result import Result


class ResultInputSerializer(ModelSerializer):
    input_id = serializers.UUIDField()

    class Meta:
        model = Result
        fields = (
            "result_type",
            "input_id"
        )


class ResultOutputSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Result
        fields = (
            "id",
            "content",
            "result_type",
            "input",
            "created_at",
            "updated_at"
        )
