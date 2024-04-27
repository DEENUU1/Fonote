from typing import Dict, Any

from ..models import Contact
from ..repositories.contact_repository import ContactRepository


class ContactService:
    """
    Service for handling contact-related operations.

    Attributes:
        contact_repository: An instance of ContactRepository for interacting with contact data.

    Methods:
        create(data: Dict[str, Any]) -> Contact:
            Creates a new contact entry with the given data.
    """

    def __init__(self):
        """
        Initialize the ContactService.
        """
        self.contact_repository = ContactRepository()

    def create(self, data: Dict[str, Any]) -> Contact:
        """
        Creates a new contact entry with the given data.

        Args:
            data (Dict[str, Any]): The data to create the contact with.

        Returns:
            Contact: The created contact object.
        """
        return self.contact_repository.create(data)
