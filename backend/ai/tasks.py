from typing import Optional

from .models.input_data import InputData
from ai.processor.youtube.youtube_processor import YoutubeProcessor
from .processor.spotify.spotify_processor import SpotifyProcessor


# TODO make this celery task


def run_youtube_processor(input_data: InputData, transcription_type: Optional[str] = None) -> None:
    youtube_processor = YoutubeProcessor(input_data, transcription_type)
    youtube_processor.process()
    return


def run_spotify_processor(input_data: InputData, transcription_type: Optional[str] = None) -> None:
    spotify_processor = SpotifyProcessor(input_data, transcription_type)
    spotify_processor.process()
    return