from ..models.contact import Contact
from rest_framework.serializers import ModelSerializer, DateTimeField


class ContactInputSerializer(ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            "name",
            "email",
            "subject",
            "message",
        )


class ContactOutputSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Contact
        fields = (
            "id",
            "name",
            "email",
            "subject",
            "message",
            "created_at",
            "updated_at"
        )
