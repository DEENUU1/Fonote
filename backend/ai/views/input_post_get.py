from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.input_data_serializers import (
    InputDataInputSerializer,
    InputDataOutputSerializer,
    InputDataListOutputSerializer
)
from ..services.input_service import InputDataService


class InputAPIView(APIView):
    """
    API view for creating and retrieving input data.

    Attributes:
        permission_classes: The permission classes required to access this view.

    Methods:
        post(request):
            Creates a new input subscription.
        get(request):
            Retrieves a list of input data associated with the authenticated user.
    """
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()

    def post(self, request):
        """
        Creates a new input subscription.

        Args:
            request: The request object.

        Returns:
            Response: The serialized data of the created input data with HTTP status code 201 (Created).
        """
        # TODO add rate limit
        serializer = InputDataInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_db = self._service.create_input_subscription(serializer.validated_data, request.user)
        return Response(InputDataOutputSerializer(input_db).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Retrieves a list of input data associated with the authenticated user.

        Args:
            request: The request object.

        Returns:
            Response: The serialized data of the input data list with HTTP status code 200 (OK).
        """
        input_data = self._service.get_input_list_by_user(request.user.id)
        return Response(InputDataListOutputSerializer(input_data, many=True).data, status=status.HTTP_200_OK)
