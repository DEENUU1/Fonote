from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.result_service import ResultService
from ..serializers.result_serializers import (
    ResultInputSerializer,
    ResultOutputSerializer,
)


class ResultCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    _service = ResultService()

    def post(self, request):
        result_serializer = ResultInputSerializer(data=request.data)
        result_serializer.is_valid(raise_exception=True)
        result_db = self._service.create(result_serializer.validated_data)
        return Response(ResultOutputSerializer(result_db).data, status=status.HTTP_201_CREATED)
