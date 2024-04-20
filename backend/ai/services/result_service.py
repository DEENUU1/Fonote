from typing import Dict, Any
from uuid import UUID
from rest_framework.exceptions import NotFound

from ..repositories.result_repository import ResultRepository
from ..repositories.input_repository import InputDataRepository


class ResultService:
    def __init__(self):
        self.result_repository = ResultRepository()
        self.input_repository = InputDataRepository()

    def create(self, data: Dict[str, Any]):
        return self.result_repository.create(data)

    def update_status(self, result_id: UUID, status: str):
        if not self.result_repository.result_exists_by_uuid(result_id):
            raise NotFound("Result not found")

        result = self.result_repository.get_result_by_uuid(result_id)
        return self.result_repository.update_status(result, status)

    def count_results_by_input_data_id(self, input_data_id: UUID) -> int:
        if not self.input_repository.input_exists_by_uuid(input_data_id):
            raise NotFound("Input data not found")

        return self.result_repository.count_results_by_input_data_id(input_data_id)
