from typing import Dict, List
from uuid import UUID

from django.contrib.auth.backends import UserModel

from ..models.input_data import InputData


class InputDataRepository:
    def __init__(self):
        self.model = InputData

    def create(self, data: Dict, user: UserModel) -> InputData:
        return self.model.objects.create(**data, user=user)

    def get_input_list_by_user(self, user: UserModel) -> List[InputData]:
        return self.model.objects.filter(user=user)

    def get_input_details_by_uuid(self, uuid: UUID) -> InputData:
        return self.model.objects.get(id=uuid)

    def input_exists_by_uuid(self, uuid: UUID) -> bool:
        return self.model.objects.filter(id=uuid).exists()

    @staticmethod
    def input_belongs_to_user(input_data: InputData, user: UserModel) -> bool:
        return input_data.user == user

    @staticmethod
    def delete(input_data: InputData) -> bool:
        return input_data.delete()

