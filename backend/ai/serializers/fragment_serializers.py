from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models.fragment import Fragment


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
