from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.input_data_serializers import InputDataOutputSerializer
from ..services.input_service import InputDataService


class InputPkAPIView(APIView):
    """
    API view to retrieve and delete input data by its UUID.

    Attributes:
        permission_classes: The permission classes required to access this view.

    Methods:
        get(request, pk):
            Retrieves details of the input data identified by the UUID.
        delete(request, pk):
            Deletes the input data identified by the UUID.
    """
    permission_classes = (IsAuthenticated,)
    _service = InputDataService()

    def get(self, request, pk):
        """
        Retrieves details of the input data identified by the UUID.

        Args:
            request: The request object.
            pk: The UUID of the input data.

        Returns:
            Response: The serialized data of the input data.
        """
        input_data = self._service.get_input_details_by_uuid(pk, request.user)
        return Response(InputDataOutputSerializer(input_data).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Deletes the input data identified by the UUID.

        Args:
            request: The request object.
            pk: The UUID of the input data.

        Returns:
            Response: A response with HTTP status code 204 (No Content).
        """
        self._service.delete(pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
