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
