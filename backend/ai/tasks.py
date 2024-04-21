from .models.input_data import InputData
from .sources.youtube_processor import YoutubeProcessor
from time import sleep


def run_youtube_processor(input_data: InputData):
    # TODO later change this and first set `instance.status = "PROCESSING"` and then
    # run the Celery task to process
    if input_data.source == "YOUTUBE" and input_data.status == "PROCESSING":
        youtube_processor = YoutubeProcessor(input_data)
        youtube_processor.process()
        sleep(5)
