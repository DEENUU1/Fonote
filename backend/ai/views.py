from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import InputDataInputSerializer, InputDataListOutputSerializer, InputDataOutputSerializer
from .services.input_service import InputDataService


class InputAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()

    def post(self, request):
        serializer = InputDataInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._service.create_input_subscription(serializer.validated_data, request.user)
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        input_data = self._service.get_input_list_by_user(request.user.id)
        return Response(InputDataListOutputSerializer(input_data, many=True).data, status=status.HTTP_200_OK)


class InputPkAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()

    def get(self, request, pk):
        input_data = self._service.get_input_details_by_uuid(pk, request.user)
        return Response(InputDataOutputSerializer(input_data).data, status=status.HTTP_200_OK)
