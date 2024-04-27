from typing import Dict, Any
from uuid import UUID

from ..models.fragment import Fragment


class FragmentRepository:
    """A repository class for managing fragments.

    This class provides methods for creating and retrieving fragments.

    Attributes:
        model (type): The model class representing a fragment.
    """

    def __init__(self):
        """Initialize the FragmentRepository."""
        self.model = Fragment

    def create(self, data: Dict[str, Any]) -> Fragment:
        """Create a new fragment.

        Args:
            data (Dict[str, Any]): A dictionary containing data for creating the fragment.

        Returns:
            Any: The created fragment object.
        """
        return self.model.objects.create(**data)

    def get_text_by_input_data_id(self, input_data_id: UUID) -> str:
        """Retrieve text by input data ID.

        Args:
            input_data_id (UUID): The ID of the input data.

        Returns:
            str: The concatenated text of fragments associated with the input data ID.
        """
        fragments = self.model.objects.filter(input_data_id=input_data_id).order_by('order')
        full_text = ''.join(fragment.text for fragment in fragments)
        return full_text
