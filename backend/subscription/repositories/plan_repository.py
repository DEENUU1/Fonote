from typing import List
from uuid import UUID

from ..models.plan import Plan


class PlanRepository:
    """
    Repository for interacting with plan data.

    Methods:
        get_active_plan_list() -> List[Plan]:
            Retrieves a list of active plans.

        get_plan_by_uuid(_id: UUID) -> Plan:
            Retrieves a plan by its UUID.

        plan_exists_by_uuid(_id: UUID) -> bool:
            Checks if a plan with the given UUID exists.

    Attributes:
        model: The Plan model used for database operations.
    """

    def __init__(self):
        """
        Initialize the PlanRepository.
        """
        self.model = Plan

    def get_active_plan_list(self) -> List[Plan]:
        """
        Retrieves a list of active plans.

        Returns:
            List[Plan]: A list of active plans.
        """
        plans = self.model.objects.filter(active=True).all()
        return plans

    def get_plan_by_uuid(self, _id: UUID) -> Plan:
        """
        Retrieves a plan by its UUID.

        Args:
            _id (UUID): The UUID of the plan.

        Returns:
            Plan: The plan object.
        """
        return self.model.objects.get(id=_id)

    def plan_exists_by_uuid(self, _id: UUID) -> bool:
        """
        Checks if a plan with the given UUID exists.

        Args:
            _id (UUID): The UUID of the plan.

        Returns:
            bool: True if the plan exists, False otherwise.
        """
        return self.model.objects.filter(id=_id).exists()
