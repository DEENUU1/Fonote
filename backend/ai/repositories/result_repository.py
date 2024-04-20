from typing import Dict, Any
from uuid import UUID

from ..models.result import Result


class ResultRepository:
    def __init__(self):
        self.model = Result

    def create(self, data: Dict[str, Any]):
        return self.model.objects.create(**data)

    @staticmethod
    def update_status(result: Result, status: str):
        result.status = status
        result.save()
        return result

    def count_results_by_input_data_id(self, input_data_id: UUID) -> int:
        return self.model.objects.filter(input_id=input_data_id).count()

    def result_exists_by_uuid(self, uuid: UUID) -> bool:
        return self.model.objects.filter(id=uuid).exists()

    def get_result_by_uuid(self, uuid: UUID) -> Result:
        return self.model.objects.get(id=uuid)
