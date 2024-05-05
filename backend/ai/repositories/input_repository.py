from datetime import datetime
from typing import Dict, List, Any
from uuid import UUID

from django.contrib.auth.backends import UserModel
from django.db.models import Q

from ..models.input_data import InputData


class InputDataRepository:
    """A repository class for managing input data.

    This class provides methods for creating, retrieving, updating, and deleting input data.

    Attributes:
        model (type): The model class representing input data.
    """

    def __init__(self):
        """Initialize the InputDataRepository."""
        self.model = InputData

    def create(self, data: Dict[str, Any], user: UserModel, source: str) -> InputData:
        """Create a new input data.

        Args:
            data (Dict[str, Any]): A dictionary containing data for creating the input data.
            user (UserModel): The user associated with the input data.
            source (str): The source of the input data.

        Returns:
            InputData: The created input data object.
        """
        return self.model.objects.create(**data, user=user, source=source)

    def get_input_list_by_user(self, user: UserModel) -> List[InputData]:
        """Retrieve a list of input data by user.

        Args:
            user (UserModel): The user associated with the input data.

        Returns:
            List[InputData]: A list of input data objects associated with the user.
        """
        return self.model.objects.filter(user=user)

    def get_input_details_by_uuid(self, uuid: UUID) -> InputData:
        """Retrieve input data details by UUID.

        Args:
            uuid (UUID): The UUID of the input data.

        Returns:
            InputData: The input data object with details.
        """
        return self.model.objects.prefetch_related('fragments').get(id=uuid)

    def input_exists_by_uuid(self, uuid: UUID) -> bool:
        """Check if input data exists by UUID.

        Args:
            uuid (UUID): The UUID of the input data.

        Returns:
            bool: True if the input data exists, False otherwise.
        """
        return self.model.objects.filter(id=uuid).exists()

    def count_user_monthly_usage(self, user: UserModel) -> int:
        """Count the number of input data created by a user in the current month.

        Args:
            user (UserModel): The user associated with the input data.

        Returns:
            int: The number of input data created by XXX user in the current month.
        """
        current_month = datetime.now().month
        return self.model.objects.filter(
            Q(user=user) &
            Q(created_at__month=current_month) &
            (Q(status='DONE') | Q(status='PROCESSING'))
        ).count()

    @staticmethod
    def input_belongs_to_user(input_data: InputData, user: UserModel) -> bool:
        """Check if input data belongs to a specific user.

        Args:
            input_data (InputData): The input data object to check.
            user (UserModel): The user to compare with.

        Returns:
            bool: True if the input data belongs to the user, False otherwise.
        """
        return input_data.user == user

    @staticmethod
    def delete(input_data: InputData) -> bool:
        """Delete input data.

        Args:
            input_data (InputData): The input data object to delete.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        return input_data.delete()

    @staticmethod
    def partial_update(data: Dict[str, Any], input_data: InputData) -> InputData:
        """Partially update input data.

        Args:
            data (Dict[str, Any]): A dictionary containing the data to update.
            input_data (InputData): The input data object to update.

        Returns:
            InputData: The updated input data object.
        """
        for key, value in data.items():
            setattr(input_data, key, value)
        input_data.save()
        return input_data

    @staticmethod
    def update_status(input_data: InputData, status: str) -> InputData:
        """Update the status of input data.

        Args:
            input_data (InputData): The input data object to update.
            status (str): The new status for the input data.

        Returns:
            InputData: The input data object with updated status.
        """
        input_data.status = status
        input_data.save()
        return input_data
