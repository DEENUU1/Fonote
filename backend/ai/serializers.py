from .models.input_data import InputData
from rest_framework.serializers import ModelSerializer, DateTimeField, SerializerMethodField
from .models.fragment import Fragment
from .models.result import Result
from rest_framework import serializers


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
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['start_time'] = self.convert_time(instance.start_time)
        representation['end_time'] = self.convert_time(instance.end_time)
        return representation

    def get_start_time(self, obj):
        return self.convert_time(obj.start_time)

    def get_end_time(self, obj):
        return self.convert_time(obj.end_time)

    def convert_time(self, time_in_seconds):
        hours = int(time_in_seconds // 3600)
        minutes = int((time_in_seconds % 3600) // 60)
        seconds = int(time_in_seconds % 60)
        return {'hours': hours, 'minutes': minutes, 'seconds': seconds}

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
