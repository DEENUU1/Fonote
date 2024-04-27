from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models.fragment import Fragment


class FragmentInputSerializer(ModelSerializer):
    """Serializer for fragment input data.

    This serializer is used to serialize fragment input data.

    Attributes:
        Meta (class): Inner class specifying metadata options for the serializer.
    """

    class Meta:
        """Metadata options for the FragmentInputSerializer."""

        model = Fragment
        fields = (
            "start_time",
            "end_time",
            "order",
            "text",
            "input_data"
        )


class FragmentOutputSerializer(ModelSerializer):
    """Serializer for fragment output data.

    This serializer is used to serialize fragment output data, including converting
    start_time and end_time to a dictionary representing hours, minutes, and seconds.

    Attributes:
        Meta (class): Inner class specifying metadata options for the serializer.
    """

    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    def to_representation(self, instance):
        """Converts the instance to a representation, converting start_time and end_time.

        Args:
            instance: The instance of the model.

        Returns:
            dict: A dictionary representing the serialized instance.
        """
        representation = super().to_representation(instance)
        representation['start_time'] = self.convert_time(instance.start_time)
        representation['end_time'] = self.convert_time(instance.end_time)
        return representation

    def get_start_time(self, obj):
        """Retrieve the start time of the fragment.

        Args:
            obj: The instance of the model.

        Returns:
            dict: A dictionary representing the start time.
        """
        return self.convert_time(obj.start_time)

    def get_end_time(self, obj):
        """Retrieve the end time of the fragment.

        Args:
            obj: The instance of the model.

        Returns:
            dict: A dictionary representing the end time.
        """
        return self.convert_time(obj.end_time)

    def convert_time(self, time_in_seconds):
        """Convert time in seconds to hours, minutes, and seconds.

        Args:
            time_in_seconds (float): Time in seconds.

        Returns:
            dict: A dictionary representing hours, minutes, and seconds.
        """
        hours = int(time_in_seconds // 3600)
        minutes = int((time_in_seconds % 3600) // 60)
        seconds = int(time_in_seconds % 60)
        return {'hours': hours, 'minutes': minutes, 'seconds': seconds}

    class Meta:
        """Metadata options for the FragmentOutputSerializer."""

        model = Fragment
        fields = (
            "id",
            "start_time",
            "end_time",
            "order",
            "text",
            "input_data"
        )
