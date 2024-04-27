from typing import Dict, Any
from uuid import UUID

from django.contrib.auth.backends import UserModel
from rest_framework.exceptions import NotFound, PermissionDenied, APIException

from ..repositories.result_repository import ResultRepository
from ..repositories.input_repository import InputDataRepository
from ai.processor.llm.groq_llm import GroqLLM
from ..repositories.fragment_repository import FragmentRepository


class ResultService:
    def __init__(self):
        self.result_repository = ResultRepository()
        self.input_repository = InputDataRepository()
        self.fragment_repository = FragmentRepository()

    def create(self, data: Dict[str, Any]):
        if not self.input_repository.input_exists_by_uuid(data.get("input_id")):
            raise NotFound("Input data not found!")

        input_text = self.fragment_repository.get_text_by_input_data_id(data.get("input_id"))
        input_obj = self.input_repository.get_input_details_by_uuid(data.get("input_id"))

        groq = GroqLLM()
        llm_response = groq.generate(data.get("result_type"), input_text, input_obj.language)

        if not llm_response:
            raise APIException("Failed to generate response :(")

        return self.result_repository.create(data, llm_response)

    def get_result_list_by_input_data_id(self, input_data_id: UUID, user: UserModel):
        if not self.input_repository.input_exists_by_uuid(input_data_id):
            raise NotFound("Input data not found")

        input_data = self.input_repository.get_input_details_by_uuid(input_data_id)
        if not self.input_repository.input_belongs_to_user(input_data, user):
            raise PermissionDenied("You don't have access to this object!")

        return self.result_repository.get_result_list_by_input_data(input_data)
