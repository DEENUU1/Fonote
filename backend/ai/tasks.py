from typing import Optional

from .models.input_data import InputData
from ai.processor.youtube.youtube_processor import YoutubeProcessor

# TODO make this celery task


def run_youtube_processor(input_data: InputData, transcription_type: Optional[str] = None):
    youtube_processor = YoutubeProcessor(input_data, transcription_type)
    youtube_processor.process()
