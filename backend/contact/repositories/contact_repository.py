from typing import Dict, Any

from ..models.contact import Contact


class ContactRepository:
    def __init__(self):
        self.model = Contact

    def create(self, data: Dict[str, Any]):
        return self.model.objects.create(**data)
