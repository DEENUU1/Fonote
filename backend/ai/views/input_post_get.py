from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.input_service import InputDataService
from ..serializers.input_data_serializers import (
    InputDataInputSerializer,
    InputDataOutputSerializer,
    InputDataListOutputSerializer
)


class InputAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()

    def post(self, request):
        serializer = InputDataInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_db = self._service.create_input_subscription(serializer.validated_data, request.user)
        return Response(InputDataOutputSerializer(input_db).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        input_data = self._service.get_input_list_by_user(request.user.id)
        return Response(InputDataListOutputSerializer(input_data, many=True).data, status=status.HTTP_200_OK)
