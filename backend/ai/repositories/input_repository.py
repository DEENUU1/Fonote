from typing import Dict

from django.contrib.auth.backends import UserModel

from ..models.input_data import InputData


class InputDataRepository:
    def __init__(self):
        self.model = InputData

    def create(self, data: Dict, user: UserModel) -> InputData:
        return self.model.objects.create(**data, user=user)
