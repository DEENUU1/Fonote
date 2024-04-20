from typing import Dict, List
from uuid import UUID

from django.contrib.auth.backends import UserModel

from ..models.input_data import InputData


class InputDataRepository:
    def __init__(self):
        self.model = InputData

    def create(
            self,
            data: Dict,
            user: UserModel,
            source: str,
            audio_length: int,
            source_title: str,
            transcription_type: str,
            status: str
    ) -> InputData:
        return self.model.objects.create(
            **data,
            user=user,
            source=source,
            audio_length=audio_length,
            source_title=source_title,
            transcription_type=transcription_type,
            status=status
        )

    def get_input_list_by_user(self, user: UserModel) -> List[InputData]:
        return self.model.objects.filter(user=user)

    def get_input_details_by_uuid(self, uuid: UUID) -> InputData:
        return self.model.objects.prefetch_related('fragments').get(id=uuid)

    def input_exists_by_uuid(self, uuid: UUID) -> bool:
        return self.model.objects.filter(id=uuid).exists()

    @staticmethod
    def input_belongs_to_user(input_data: InputData, user: UserModel) -> bool:
        return input_data.user == user

    @staticmethod
    def delete(input_data: InputData) -> bool:
        return input_data.delete()

