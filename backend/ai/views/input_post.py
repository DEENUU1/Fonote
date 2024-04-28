from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.input_data_serializers import (
    InputDataInputSerializer,
    InputDataOutputSerializer,
)
from ..services.input_service import InputDataService
from ..throttle.input_create_throttle import InputCreateThrottle


class InputCreateAPIView(APIView):
    """
    API view for creating input data.

    Attributes:
        permission_classes: The permission classes required to access this view.

    Methods:
        post(request):
            Creates a new input subscription.
    """
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()
    throttle_classes = (InputCreateThrottle, )

    @swagger_auto_schema(operation_description="Create input object", request_body=InputDataInputSerializer)
    def post(self, request):
        """
        Creates a new input subscription.

        Args:
            request: The request object.

        Returns:
            Response: The serialized data of the created input data with HTTP status code 201 (Created).
        """
        serializer = InputDataInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_db = self._service.create_input_subscription(serializer.validated_data, request.user)
        return Response(InputDataOutputSerializer(input_db).data, status=status.HTTP_201_CREATED)
