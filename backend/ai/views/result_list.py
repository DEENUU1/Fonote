from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.result_serializers import ResultOutputSerializer
from ..services.result_service import ResultService


class ResultListAPIView(APIView):
    """
    API view for retrieving a list of results associated with an input data.

    Attributes:
        permission_classes: The permission classes required to access this view.

    Methods:
        get(request, pk):
            Retrieves a list of results associated with the input data identified by the UUID.
    """
    permission_classes = (IsAuthenticated,)
    _service = ResultService()

    def get(self, request, pk):
        """
        Retrieves a list of results associated with the input data identified by the UUID.

        Args:
            request: The request object.
            pk: The UUID of the input data.

        Returns:
            Response: The serialized data of the result list with HTTP status code 200 (OK).
        """
        result = self._service.get_result_list_by_input_data_id(pk, request.user)
        return Response(ResultOutputSerializer(result, many=True).data, status=status.HTTP_200_OK)
