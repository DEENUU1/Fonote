from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.plan_serializer import PlanOutputSerializer
from ..services.plan_service import PlanService


class PlanListAPIView(APIView):
    permission_classes = (AllowAny,)
    _plan_service = PlanService()

    def get(self, request):
        plans = self._plan_service.get_active_plan_list()
        return Response(
            PlanOutputSerializer(plans, many=True).data,
            status=status.HTTP_200_OK
        )
