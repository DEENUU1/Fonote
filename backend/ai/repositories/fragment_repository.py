from typing import Dict, Any
from uuid import UUID

from ..models.fragment import Fragment


class FragmentRepository:
    def __init__(self):
        self.model = Fragment

    def create(self, data: Dict[str, Any]):
        return self.model.objects.create(**data)

    def get_text_by_input_data_id(self, input_data_id: UUID):
        fragments = self.model.objects.filter(input_data_id=input_data_id).order_by('order')
        full_text = ''.join(fragment.text for fragment in fragments)
        return full_text
