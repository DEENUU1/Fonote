from ai.models.input_data import InputData
from django.contrib.auth.backends import UserModel
import pytest


@pytest.fixture()
def user_instance():
    return UserModel.objects.create_user(username="XXXXXXXX", password="XXXXXXXXXXXX")


@pytest.fixture()
def input_data_instance(user_instance):
    return InputData.objects.create(
        source="YOUTUBE",
        transcription_type="LLM",
        audio_length=60,
        source_title="test source title",
        status="DONE",
        language="Polish",
        user=user_instance
    )


@pytest.mark.django_db
def test_input_data_instance(input_data_instance):
    assert input_data_instance.source == "YOUTUBE"
    assert input_data_instance.transcription_type == "LLM"
    assert input_data_instance.audio_length == 60
    assert input_data_instance.source_title == "test source title"
    assert input_data_instance.status == "DONE"
    assert input_data_instance.language == "Polish"
