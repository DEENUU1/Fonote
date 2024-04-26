import os
from typing import Optional

from pydub import AudioSegment
from openai import OpenAI
import logging
from utils.get_date_hash import get_date_hash
from django.conf import settings


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

    def split_audio_to_chunks(self) -> Optional[str]:
        try:
            audio = AudioSegment.from_file(self.audio_file_path)

            chunk_length = self.chunk_size * 1000
            chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

            logging.info(f"Split file into {len(chunks)} chunks")

            date_hash = get_date_hash()
            output_directory = f"{settings.AUDIO_CHUNK_FILE_PATH}{date_hash}"
            os.makedirs(output_directory, exist_ok=True)

            for i, chunk in enumerate(chunks):
                chunk.export(os.path.join(output_directory, f"chunk_{i}.mp3"), format="mp3")
                logger.info(f"Chunk {i} exported")

            return output_directory

        except Exception as e:
            logger.error(f"Error while splitting audio file: {e}")
            return

    def transcribe_audio(self, audio_file) -> Optional[str]:
        try:
            transcription = self.client.audio.transcriptions.create(
                model=self.whisper_model,
                file=audio_file,
            )
            return transcription.text
        except Exception as e:
            logger.error(f"Error while transcribing audio: {e}")
            return

    def run(self) -> Optional[str]:
        result = ""

        audio_path = self.split_audio_to_chunks()
        if not audio_path:
            return None

        sorted_chunks = sorted(os.listdir(audio_path), key=self.numerical_sort)
        for chunk in sorted_chunks:
            chunk_path = f"{audio_path}/{chunk}"
            transcription = self.transcribe_audio(chunk_path)
            if not transcription:
                continue
            result += transcription

            logger.info(f"Transcribed chunk {chunk}")

            os.remove(chunk_path)

            logger.info(f"Removed chunk {chunk}")

        return result
