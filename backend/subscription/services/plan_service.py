from ..serializers.plan_serializer import PlanOutputSerializer
from ..repositories.plan_repository import PlanRepository


class PlanService:
    def __init__(self):
        self.plan_repository = PlanRepository()

    def get_active_plan_list(self):
        plans = self.plan_repository.get_active_plan_list()
        return PlanOutputSerializer(plans, many=True).data
