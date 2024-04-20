from typing import Dict, Any, Optional, List
from uuid import UUID

from django.contrib.auth.backends import UserModel
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound

from subscription.repositories.plan_repository import PlanRepository
from subscription.repositories.user_subscription_repository import UserSubscriptionRepository
from ..models import InputData
from ..repositories.fragment_repository import FragmentRepository
from ..repositories.input_repository import InputDataRepository
from ..serializers import FragmentInputSerializer
from ..sources.youtube_data import get_youtube_video_data
from ..sources.youtube_transcription import YoutubeTranscription


class InputDataService:
    def __init__(self):
        self.input_repository = InputDataRepository()
        self.user_subscription_repository = UserSubscriptionRepository()
        self.plan_repository = PlanRepository()
        self.fragment_repository = FragmentRepository()

    @staticmethod
    def get_source_from_url(url: str) -> Optional[str]:
        if "spotify" in url:
            return "SPOTIFY"

        if "youtube" in url:
            return "YOUTUBE"

        return None

    def create_input_subscription(self, data: Dict[str, Any], user: UserModel):
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
                raise ValidationError("LLM transcription is not available yet")

            input_db = self.input_repository.create(
                data=data,
                user=user,
                source=source,
                audio_length=video_data.get("length"),
                source_title=video_data.get("title"),
                transcription_type=transcription_type,
                status="DONE"
            )

            formatted = youtube_transcript.format_text(transcription)

            for idx, txt in enumerate(formatted):
                data = {
                    "start_time": txt.start_time,
                    "end_time": txt.end_time,
                    "order": idx,
                    "text": txt.transcriptions,
                    "input_data": input_db.id
                }
                fragment_serializer = FragmentInputSerializer(data=data)
                fragment_serializer.is_valid(raise_exception=True)
                self.fragment_repository.create(fragment_serializer.validated_data)

            # TODO run task to generate LLM response and save to Result object

        if source == "SPOTIFY":
            if not plan.ai_transcription:
                raise ValidationError("You can't use LLM transcription generator")

            raise ValidationError("Spotify is not supported yet")

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
