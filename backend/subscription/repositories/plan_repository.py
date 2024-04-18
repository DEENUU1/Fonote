from ..models.plan import Plan
from ..serializers.plan_serializer import PlanOutputSerializer


class PlanRepository:
    def __init__(self):
        self.model = Plan

    def get_active_plan_list(self):
        plans = self.model.objects.filter(active=True).all()
        serializer = PlanOutputSerializer(plans, many=True).data
        return serializer

    def get_plan_by_price_id(self, price_id: str):
        plan = self.model.objects.get(price_id=price_id)
        return PlanOutputSerializer(plan).data
