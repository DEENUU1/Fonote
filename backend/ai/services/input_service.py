from django.contrib.auth.backends import UserModel

from ..repositories.input_repository import InputDataRepository
from ..serializers import InputDataOutputSerializer
from typing import Dict


class InputDataService:
    def __init__(self):
        self.input_repository = InputDataRepository()

    def create(self, data: Dict, user: UserModel) -> InputDataOutputSerializer:
        return self.input_repository.create(data, user)


