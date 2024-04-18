from django.contrib.auth.backends import UserModel

from ..models.input_data import InputData
from ..serializers import InputDataOutputSerializer
from typing import Dict


class InputDataRepository:
    def __init__(self):
        self.model = InputData

    def create(self, data: Dict, user: UserModel) -> InputDataOutputSerializer:
        input_data = self.model.objects.create(
            **data,
            user=user
        )
        return InputDataOutputSerializer(input_data)



