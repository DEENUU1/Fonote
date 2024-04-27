from rest_framework.serializers import ModelSerializer, DateTimeField

from ..models.contact import Contact


class ContactInputSerializer(ModelSerializer):
    """
    Serializer for handling input data when creating a contact.

    Attributes:
        Meta:
            model (Contact): The Contact model.
            fields (tuple): The fields to include in the serializer.
    """

    class Meta:
        """
        Metadata class for the ContactInputSerializer.
        """
        model = Contact
        fields = (
            "name",
            "email",
            "subject",
            "message",
        )


class ContactOutputSerializer(ModelSerializer):
    """
    Serializer for serializing contact data for output.

    Attributes:
        created_at (DateTimeField): The field representing the creation date and time.
        updated_at (DateTimeField): The field representing the last update date and time.

    Meta:
        model (Contact): The Contact model.
        fields (tuple): The fields to include in the serializer.
    """
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """
        Metadata class for the ContactOutputSerializer.
        """
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
