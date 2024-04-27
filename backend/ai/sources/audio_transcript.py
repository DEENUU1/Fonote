import logging
import os
from typing import Optional, List

from django.conf import settings
from openai import OpenAI
from openai.types.audio import Transcription
from pydub import AudioSegment
from .fragment import Fragment
from .fragment_list import FragmentList
from utils.get_date_hash import get_date_hash

logger = logging.getLogger(__name__)


class AudioTranscription:
    def __init__(self, audio_file_path: str, chunk_size: int = 150):
        self.audio_file_path = audio_file_path
        self.whisper_model = "whisper-1"
        self.chunk_size = chunk_size
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def numerical_sort(chunk) -> int:
        return int(chunk.split('_')[1].split('.')[0])

    @staticmethod
    def get_audio_file(path: str):
        try:
            audio_file = open(path, "rb")
            return audio_file

        except Exception as e:
            logger.error(f"Error while opening file: {e}")

    def transcribe_audio(self, audio_file, language: str) -> Optional[Transcription]:
        try:
            transcription = self.client.audio.transcriptions.create(
                model=self.whisper_model,
                file=audio_file,
                language=language,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
            return transcription
        except Exception as e:
            logger.error(f"Error while transcribing audio: {e}")
            return

    def format_text(self, full_text) -> List[Fragment]:
        fragments = []
        current_fragment = None

        for text in full_text.words:
            if current_fragment is None:
                current_fragment = Fragment(
                    start_time=text["start"],
                    end_time=text["start"] + text["end"] - text["start"],
                    transcriptions=text["word"]
                )
            else:
                if text["word"].endswith("."):
                    current_fragment.transcriptions += " " + text["word"]
                    fragments.append(current_fragment)
                    current_fragment = None
                else:
                    current_fragment.transcriptions += " " + text["word"]
                    current_fragment.end_time = text["start"] + text["end"] - text["start"]

        if current_fragment is not None:
            fragments.append(current_fragment)

        return fragments

    def run(self, language: str) -> Optional[FragmentList]:
        audio_file = self.get_audio_file(self.audio_file_path)
        transcription = self.transcribe_audio(audio_file, language)
        if not transcription:
            logger.info("Couldn't transcribe audio file")
            return None

        logger.info("Transcribe audio file")

        formatted_text = self.format_text(transcription)

        logger.info(f"Format transcription")

        return FragmentList(type_="LLM", fragments=formatted_text)

