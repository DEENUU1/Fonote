from django.contrib.auth.backends import UserModel

from ..repositories.input_repository import InputDataRepository
from typing import Dict
from ..models import InputData


class InputDataService:
    def __init__(self):
        self.input_repository = InputDataRepository()

    def create(self, data: Dict, user: UserModel) -> InputData:
        return self.input_repository.create(data, user)


