from typing import List
from uuid import UUID

from rest_framework.exceptions import NotFound

from ..models import Plan
from ..repositories.plan_repository import PlanRepository


class PlanService:
    """
    Service class for managing plans.

    Attributes:
        plan_repository (PlanRepository): The repository for interacting with plans.

    Methods:
        get_active_plan_list() -> List[Plan]:
            Retrieves a list of active plans.

        get_plan_by_id(plan_id: UUID) -> Plan:
            Retrieves a plan by its ID.
    """

    def __init__(self):
        """
        Initializes the PlanService with the PlanRepository.
        """
        self.plan_repository = PlanRepository()

    def get_active_plan_list(self) -> List[Plan]:
        """
        Retrieves a list of active plans.

        Returns:
            List[Plan]: A list of active plans.
        """
        return self.plan_repository.get_active_plan_list()

    def get_plan_by_id(self, plan_id: UUID) -> Plan:
        """
        Retrieves a plan by its ID.

        Args:
            plan_id (UUID): The ID of the plan to retrieve.

        Returns:
            Plan: The plan with the specified ID.

        Raises:
            NotFound: If the plan with the specified ID does not exist.
        """
        if not self.plan_repository.plan_exists_by_uuid(plan_id):
            raise NotFound(detail="Plan not found")

        return self.plan_repository.get_plan_by_uuid(plan_id)
