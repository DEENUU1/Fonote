from ..models.plan import Plan
from ..serializers.plan_serializer import PlanOutputSerializer


class PlanRepository:
    def __init__(self):
        self.model = Plan

    def get_active_plan_list(self):
        plans = self.model.objects.filter(active=True)
        serializer = PlanOutputSerializer(plans, many=True)
        return serializer.data
