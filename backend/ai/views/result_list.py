from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.result_service import ResultService
from ..serializers.result_serializers import ResultOutputSerializer


class ResultListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _service = ResultService()

    def get(self, request, pk):
        result = self._service.get_result_list_by_input_data_id(pk, request.user)
        return Response(ResultOutputSerializer(result, many=True).data, status=status.HTTP_200_OK)
