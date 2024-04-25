from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.input_service import InputDataService
from ..serializers.input_data_serializers import InputDataOutputSerializer


class InputPkAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()

    def get(self, request, pk):
        input_data = self._service.get_input_details_by_uuid(pk, request.user)
        return Response(InputDataOutputSerializer(input_data).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        self._service.delete(pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
