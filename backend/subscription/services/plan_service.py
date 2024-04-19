from typing import List

from ..models import Plan
from ..repositories.plan_repository import PlanRepository


class PlanService:
    def __init__(self):
        self.plan_repository = PlanRepository()

    def get_active_plan_list(self) -> List[Plan]:
        return self.plan_repository.get_active_plan_list()

    def get_plan_by_price_id(self, price_id: str) -> Plan:
        return self.plan_repository.get_plan_by_price_id(price_id)
