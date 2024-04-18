from django.contrib.auth.backends import UserModel

from ..repositories.input_repository import InputDataRepository
from ..serializers import InputDataInputSerializer, InputDataOutputSerializer


class InputDataService:
    def __init__(self):
        self.input_repository = InputDataRepository()

    def create(self, data: InputDataInputSerializer, user: UserModel) -> InputDataOutputSerializer:
        return self.input_repository.create(data, user)


