from typing import Optional
from uuid import UUID

from ai.processor.youtube.youtube_processor import YoutubeProcessor
from .processor.spotify.spotify_processor import SpotifyProcessor
from celery import shared_task
from .repositories.input_repository import InputDataRepository


@shared_task()
def run_processor(input_data_id: UUID, source: str, transcription_type: Optional[str] = None) -> None:
    input_data = InputDataRepository().get_input_details_by_uuid(input_data_id)

    if source == "YOUTUBE":
        youtube_processor = YoutubeProcessor(input_data, transcription_type)
        youtube_processor.process()
        return

    elif source == "SPOTIFY":
        spotify_processor = SpotifyProcessor(input_data, transcription_type)
        spotify_processor.process()
        return

    return
