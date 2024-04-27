from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.input_data_serializers import (
    InputDataListOutputSerializer
)
from ..services.input_service import InputDataService


class InputListAPIView(APIView):
    """
    API view for retrieving input data.

    Attributes:
        permission_classes: The permission classes required to access this view.

    Methods:
        get(request):
            Retrieves a list of input data associated with the authenticated user.
    """
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()

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
