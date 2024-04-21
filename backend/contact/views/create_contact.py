from rest_framework.views import APIView
from ..serializers.contact_serializer import ContactInputSerializer, ContactOutputSerializer
from ..services.contact_service import ContactService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class ContactCreateAPIView(APIView):
    permission_classes = (AllowAny,)
    _contact_service = ContactService()

    def post(self, request):
        serializer = ContactInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = self._contact_service.create(serializer.validated_data)
        return Response(ContactOutputSerializer(contact).data, status=status.HTTP_201_CREATED)
