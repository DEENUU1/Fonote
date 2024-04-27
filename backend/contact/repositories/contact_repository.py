from typing import Dict, Any

from ..models.contact import Contact


class ContactRepository:
    """
    Repository for interacting with contact data.

    Methods:
        create(data: Dict[str, Any]) -> Contact:
            Creates a new contact entry with the given data.

    Attributes:
        model: The Contact model used for database operations.
    """

    def __init__(self):
        """
        Initialize the ContactRepository.
        """
        self.model = Contact

    def create(self, data: Dict[str, Any]) -> Contact:
        """
        Creates a new contact entry with the given data.

        Args:
            data (Dict[str, Any]): The data to create the contact with.

        Returns:
            Contact: The created contact object.
        """
        return self.model.objects.create(**data)
