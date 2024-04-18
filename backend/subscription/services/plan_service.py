from ..repositories.plan_repository import PlanRepository


class PlanService:
    def __init__(self):
        self.plan_repository = PlanRepository()

    def get_active_plan_list(self):
        return self.plan_repository.get_active_plan_list()
