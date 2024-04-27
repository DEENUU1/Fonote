from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.result_serializers import (
    ResultInputSerializer,
    ResultOutputSerializer,
)
from ..services.result_service import ResultService
from ..throttle.result_create_throttle import ResultCreateThrottle


class ResultCreateAPIView(APIView):
    """
    API view for creating a result.

    Attributes:
        permission_classes: The permission classes required to access this view.

    Methods:
        post(request):
            Creates a new result.
    """
    permission_classes = (IsAuthenticated,)
    _service = ResultService()
    throttle_classes = (ResultCreateThrottle, )

    def post(self, request):
        """
        Creates a new result.

        Args:
            request: The request object.

        Returns:
            Response: The serialized data of the created result with HTTP status code 201 (Created).
        """
        result_serializer = ResultInputSerializer(data=request.data)
        result_serializer.is_valid(raise_exception=True)
        result_db = self._service.create(result_serializer.validated_data)
        return Response(ResultOutputSerializer(result_db).data, status=status.HTTP_201_CREATED)
