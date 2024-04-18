from django.contrib.auth.backends import UserModel

from ..models import InputData
from ..serializers import InputDataInputSerializer, InputDataOutputSerializer


class InputDataRepository:
    def __init__(self):
        self.model = InputData

    def create(self, data: InputDataInputSerializer, user: UserModel) -> InputDataOutputSerializer:
        input_data = self.model.objects.create(
            **data,
            user=user
        )
        return InputDataOutputSerializer(input_data)



