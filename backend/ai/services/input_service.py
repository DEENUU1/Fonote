from typing import Dict, Any, Optional, List
from uuid import UUID

from django.contrib.auth.backends import UserModel
from rest_framework.exceptions import PermissionDenied, NotFound, APIException

from subscription.repositories.plan_repository import PlanRepository
from subscription.repositories.user_subscription_repository import UserSubscriptionRepository
from ..models import InputData
from ..repositories.fragment_repository import FragmentRepository
from ..repositories.input_repository import InputDataRepository
from ..repositories.result_repository import ResultRepository
from ..tasks import run_processor


class InputDataService:
    def __init__(self):
        self.input_repository = InputDataRepository()
        self.user_subscription_repository = UserSubscriptionRepository()
        self.plan_repository = PlanRepository()
        self.fragment_repository = FragmentRepository()
        self.result_repository = ResultRepository()

    @staticmethod
    def get_source_from_url(url: str) -> Optional[str]:
        if "spotify.com/" in url:
            return "SPOTIFY"

        if "youtube.com/" in url:
            return "YOUTUBE"

        return None

    def create_input_subscription(self, data: Dict[str, Any], user: UserModel) -> InputData:
        user_subscription = self.user_subscription_repository.get_current_subscription_by_user(user)

        if user_subscription is None:
            raise PermissionDenied("You don't have access!")

        if not self.plan_repository.plan_exists_by_uuid(user_subscription.plan.id):
            raise NotFound("Plan not found, please contact with support.")

        plan = self.plan_repository.get_plan_by_uuid(user_subscription.plan.id)
        source = self.get_source_from_url(data.get("source_url"))

        transcription_type = data.get("transcription_type")
        language = data.get("language")

        if transcription_type not in ["GENERATED", "MANUAL"] and not plan.ai_transcription:
            raise PermissionDenied("Your subscription doesn't allow you to process data from AI")

        if transcription_type == "LLM" and source == "SPOTIFY":
            raise APIException("Not implemented!")

        if not plan.change_lang and language != "English":
            raise PermissionDenied("Your subscription doesn't allow you to change language")

        if source == "SPOTIFY" and not plan.spotify:
            raise PermissionDenied("Your subscription doesn't allow you to process data from Spotify")

        if source == "YOUTUBE" and not plan.youtube:
            raise PermissionDenied("Your subscription doesn't allow you to process data from Youtube")

        input_data_db = self.input_repository.create(data=data, user=user, source=source)
        self.input_repository.update_status(input_data_db, "PROCESSING")
        # run_processor.delay(input_data_db.pk, source, transcription_type)
        run_processor(input_data_db.pk, source, transcription_type)
        return input_data_db

    def get_input_list_by_user(self, user: UserModel) -> List[InputData]:
        return self.input_repository.get_input_list_by_user(user)

    def get_input_details_by_uuid(self, _id: UUID, user: UserModel) -> InputData:
        if not self.input_repository.input_exists_by_uuid(_id):
            raise NotFound("Input not found")

        input_data = self.input_repository.get_input_details_by_uuid(_id)

        if not self.input_repository.input_belongs_to_user(input_data, user):
            raise PermissionDenied("You don't have access to this object!")

        return input_data

    def delete(self, _id: UUID, user: UserModel) -> bool:
        if not self.input_repository.input_exists_by_uuid(_id):
            raise NotFound("Input not found")

        input_data = self.input_repository.get_input_details_by_uuid(_id)

        if not self.input_repository.input_belongs_to_user(input_data, user):
            raise PermissionDenied("You don't have access to this object!")

        return self.input_repository.delete(input_data)
