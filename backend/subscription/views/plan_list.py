from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.plan_serializer import PlanOutputSerializer
from ..services.plan_service import PlanService


class PlanListAPIView(APIView):
    """
    API view for retrieving a list of active plans.

    Attributes:
        permission_classes (tuple): Tuple containing AllowAny permission class.
        _plan_service (PlanService): Instance of PlanService for handling plan-related operations.

    Methods:
        get(request) -> Response:
            Retrieves a list of active plans.
    """

    permission_classes = (AllowAny,)
    _plan_service = PlanService()

    def get(self, request):
        """
        Retrieves a list of active plans.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: Response containing the list of active plans.
        """
        plans = self._plan_service.get_active_plan_list()
        return Response(
            PlanOutputSerializer(plans, many=True).data,
            status=status.HTTP_200_OK
        )
