from django.contrib.auth.backends import UserModel

from ..repositories.input_repository import InputDataRepository
from typing import Dict, Any, Optional, List
from ..models import InputData
from subscription.repositories.user_subscription_repository import UserSubscriptionRepository
from subscription.repositories.plan_repository import PlanRepository
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from ..sources.youtube_transcription import YoutubeTranscription
from uuid import UUID
from ..sources.youtube_data import get_youtube_video_data


class InputDataService:
    def __init__(self):
        self.input_repository = InputDataRepository()
        self.user_subscription_repository = UserSubscriptionRepository()
        self.plan_repository = PlanRepository()

    @staticmethod
    def get_source_from_url(url: str) -> Optional[str]:
        if "spotify" in url:
            return "SPOTIFY"

        if "youtube" in url:
            return "YOUTUBE"

        return None

    def create_input_subscription(self, data: Dict[str, Any], user: UserModel) -> InputData:
        user_subscription = self.user_subscription_repository.get_current_subscription_by_user(user)

        if user_subscription is None:
            raise PermissionDenied("You don't have access to use this")

        if not self.plan_repository.plan_exists_by_uuid(user_subscription.plan.id):
            raise ValidationError("Plan not found")

        plan = self.plan_repository.get_plan_by_uuid(user_subscription.plan.id)

        source = self.get_source_from_url(data.get("source_url"))

        if source not in ["SPOTIFY", "YOUTUBE"]:
            raise ValidationError("Invalid url")

        if source == "SPOTIFY" and not plan.spotify:
            raise ValidationError("Your subscription doesn't allow you to process data from Spotify")

        if source == "YOUTUBE" and not plan.youtube:
            raise ValidationError("Your subscription doesn't allow you to process data from Youtube")

        if source == "YOUTUBE":
            video_data = get_youtube_video_data(data.get("source_url"))
            if video_data.get("length") > plan.max_length:
                raise ValidationError("Youtube video is too long")

            youtube_transcript = YoutubeTranscription(data.get("source_url"))
            video_id = youtube_transcript.get_youtube_video_id(data.get("source_url"))

            transcription, transcription_type = youtube_transcript.get_youtube_transcription(
                video_id,
                data.get("language")
            )

            if transcription is None:

                if not plan.ai_transcription:
                    raise ValidationError("You can't use LLM transcription generator")

                # TODO when InputData object is created with `transcription_type=LLM` then run task to process it
                return self.input_repository.create(
                    data=data,
                    user=user,
                    source=source,
                    audio_length=video_data.get("length"),
                    source_title=video_data.get("title"),
                    transcription_type="LLM",
                    status="NEW"
                )

            formatted = youtube_transcript.format_text(transcription)
            print(formatted)
            # TODO save formatted text to database
            self.input_repository.create(
                data=data,
                user=user,
                source=source,
                audio_length=video_data.get("length"),
                source_title=video_data.get("title"),
                transcription_type=transcription_type,
                status="DONE"
            )
            # TODO run task to generate LLM response and save to Result object

        if source == "SPOTIFY":
            if not plan.ai_transcription:
                raise ValidationError("You can't use LLM transcription generator")

            raise ValidationError("Spotify is not supported yet")

    # def create_input_unsubscription(self, data: Dict, user: UserModel) -> InputData:
    #     source = self.get_source_from_url(data.get("source_url"))
    #
    #     if source is None or source != data.get("source") or source != "YOUTUBE":
    #         raise ValidationError("Source not found")
    #
    #     # TODO check video from youtube has generated or manually added transcription
    #     # TODO check video length
    #
    #     # TODO get length and title
    #
    #     return self.input_repository.create(data, user)

    def get_input_list_by_user(self, user: UserModel) -> List[InputData]:
        return self.input_repository.get_input_list_by_user(user)

    def get_input_details_by_uuid(self, _id: UUID, user: UserModel) -> InputData:
        if not self.input_repository.input_exists_by_uuid(_id):
            raise NotFound("Input not found")

        input_data = self.input_repository.get_input_details_by_uuid(_id)

        if not self.input_repository.input_belongs_to_user(input_data, user):
            raise PermissionDenied("You don't have access to use this")

        return input_data

    def delete(self, _id: UUID, user: UserModel) -> bool:
        if not self.input_repository.input_exists_by_uuid(_id):
            raise NotFound("Input not found")

        input_data = self.input_repository.get_input_details_by_uuid(_id)

        if not self.input_repository.input_belongs_to_user(input_data, user):
            raise PermissionDenied("You don't have access to use this")

        return self.input_repository.delete(input_data)
