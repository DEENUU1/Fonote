from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import InputDataInputSerializer, InputDataOutputSerializer
from .services.input_service import InputDataService


class InputAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()

    def post(self, request):
        serializer = InputDataInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_db = self._service.create(serializer.validated_data, request.user)
        return Response(InputDataOutputSerializer(input_db).data, status=status.HTTP_201_CREATED)
