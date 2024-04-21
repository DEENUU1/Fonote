from typing import Dict, Any

from ..repositories.contact_repository import ContactRepository


class ContactService:
    def __init__(self):
        self.contact_repository = ContactRepository()

    def create(self, data: Dict[str, Any]):
        return self.contact_repository.create(data)
