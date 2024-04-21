from typing import Dict, Any, Optional
from uuid import UUID

from ..models import InputData
from ..models.result import Result


class ResultRepository:
    def __init__(self):
        self.model = Result

    def create(self, data: Dict[str, Any], content: Optional[str]):
        return self.model.objects.create(**data, content=content)

    def result_exists_by_uuid(self, uuid: UUID) -> bool:
        return self.model.objects.filter(id=uuid).exists()

    def get_result_by_uuid(self, uuid: UUID) -> Result:
        return self.model.objects.get(id=uuid)

    def get_result_list_by_input_data(self, input_data: InputData):
        return self.model.objects.filter(input=input_data)
