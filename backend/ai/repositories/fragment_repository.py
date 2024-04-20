from typing import Dict, Any

from ..models.fragment import Fragment


class FragmentRepository:
    def __init__(self):
        self.model = Fragment

    def create(self, data: Dict[str, Any]):
        return self.model.objects.create(**data)
