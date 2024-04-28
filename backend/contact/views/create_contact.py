from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.contact_serializer import ContactInputSerializer, ContactOutputSerializer
from ..services.contact_service import ContactService
from ..throttle.contact_create_throttle import ContactCreateThrottle, AnonContactCreateThrottle


class ContactCreateAPIView(APIView):
    """
    API view for creating a contact entry.

    Attributes:
        permission_classes: The permission classes required to access this view.
        _contact_service: An instance of ContactService for handling contact-related operations.

    Methods:
        post(request):
            Creates a new contact entry.
    """
    permission_classes = (AllowAny,)
    _contact_service = ContactService()
    throttle_classes = (ContactCreateThrottle, AnonContactCreateThrottle)

    @swagger_auto_schema(operation_description="Create contact object", request_body=ContactInputSerializer)
    def post(self, request):
        """
        Creates a new contact entry.

        Args:
            request: The request object.

        Returns:
            Response: The serialized data of the created contact entry with HTTP status code 201 (Created).
        """
        serializer = ContactInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = self._contact_service.create(serializer.validated_data)
        return Response(ContactOutputSerializer(contact).data, status=status.HTTP_201_CREATED)
