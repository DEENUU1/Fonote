from typing import Optional

from .models.input_data import InputData
from .sources.youtube_processor import YoutubeProcessor
from time import sleep


def run_youtube_processor(input_data: InputData, transcription_type: Optional[str] = None):
    # TODO later change this and first set `instance.status = "PROCESSING"` and then
    # run the Celery task to process
    if input_data.source == "YOUTUBE" and input_data.status == "PROCESSING":
        youtube_processor = YoutubeProcessor(input_data, transcription_type)
        youtube_processor.process()
        sleep(5)
