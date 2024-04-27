from typing import Dict, Any, Optional
from uuid import UUID

from ..models import InputData
from ..models.result import Result


class ResultRepository:
    """A repository class for managing results.

    This class provides methods for creating and retrieving results.

    Attributes:
        model (type): The model class representing a result.
    """

    def __init__(self):
        """Initialize the ResultRepository."""
        self.model = Result

    def create(self, data: Dict[str, Any], content: Optional[str]) -> Result:
        """Create a new result.

        Args:
            data (Dict[str, Any]): A dictionary containing data for creating the result.
            content (Optional[str]): The content of the result.

        Returns:
            Any: The created result object.
        """
        return self.model.objects.create(**data, content=content)

    def result_exists_by_uuid(self, uuid: UUID) -> bool:
        """Check if a result exists by UUID.

        Args:
            uuid (UUID): The UUID of the result.

        Returns:
            bool: True if the result exists, False otherwise.
        """
        return self.model.objects.filter(id=uuid).exists()

    def get_result_by_uuid(self, uuid: UUID) -> Result:
        """Retrieve a result by UUID.

        Args:
            uuid (UUID): The UUID of the result.

        Returns:
            Result: The result object.
        """
        return self.model.objects.get(id=uuid)

    def get_result_list_by_input_data(self, input_data: InputData) -> Result:
        """Retrieve a list of results by input data.

        Args:
            input_data (InputData): The input data associated with the results.

        Returns:
            QuerySet: A queryset containing the results associated with the input data.
        """
        return self.model.objects.filter(input=input_data)
