from ..models.plan import Plan
from typing import List

from uuid import UUID


class PlanRepository:
    def __init__(self):
        self.model = Plan

    def get_active_plan_list(self) -> List[Plan]:
        plans = self.model.objects.filter(active=True).all()
        return plans

    def get_plan_by_price_id(self, price_id: str) -> Plan:
        return self.model.objects.get(price__stripe_id=price_id)

    def plan_exists_by_price_id(self, price_id: str) -> bool:
        return self.model.objects.filter(price__stripe_id=price_id).exists()

    def get_plan_by_uuid(self, _id: UUID) -> Plan:
        return self.model.objects.get(id=_id)

    def plan_exists_by_uuid(self, _id: UUID) -> bool:
        return self.model.objects.filter(id=_id).exists()
