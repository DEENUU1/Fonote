import logging
from typing import Optional, List, BinaryIO

from django.conf import settings
from openai import OpenAI
from openai.types.audio import Transcription

from .fragment import Fragment
from .fragment_list import FragmentList

logger = logging.getLogger(__name__)


class AudioTranscription:
    """
    A class to handle audio transcription using OpenAI models.

    Attributes:
        audio_file_path (str): The path to the audio file for transcription.
        whisper_model (str): The model to use for transcription, defaults to "whisper-1".
        chunk_size (int): The size of audio chunks for processing, defaults to 150.

    Methods:
        numerical_sort(chunk: str) -> int:
            Static method to sort audio chunks numerically based on their index.
        get_audio_file(path: str) -> Optional[BinaryIO]:
            Static method to open an audio file in binary mode.
        transcribe_audio(audio_file: BinaryIO, language: str) -> Optional[Transcription]:
            Transcribes the audio file using the specified language and returns the transcription.
        format_text(transcription: Transcription) -> List[Fragment]:
            Formats the transcription text into fragments with start and end times.
        transcribe(language: str) -> Optional[FragmentList]:
            Transcribes the audio file, formats the text, and returns a list of fragments.
    """

    def __init__(self, audio_file_path: str, whisper_model: str = "whisper-1", chunk_size: int = 150):
        """
        Initialize AudioTranscription instance.

        Args:
            audio_file_path (str): The path to the audio file.
            whisper_model (str): The name of the whisper model to be used, defaults to "whisper-1".
            chunk_size (int): The size of audio chunks for processing, defaults to 150.

        Raises:
            ValueError: If OPENAI_API_KEY is not set in Django settings.
        """
        self.audio_file_path = audio_file_path
        self.whisper_model = whisper_model
        self.chunk_size = chunk_size

        if not settings.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY is not set in Django settings.")

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    @staticmethod
    def numerical_sort(chunk: str) -> int:
        """
        Static method to sort audio chunks numerically based on their index.

        Args:
            chunk (str): The name of the audio chunk.

        Returns:
            int: The numerical index extracted from the chunk name.
        """
        return int(chunk.split('_')[1].split('.')[0])

    @staticmethod
    def get_audio_file(path: str) -> Optional[BinaryIO]:
        """
        Static method to open an audio file in binary mode.

        Args:
            path (str): The path to the audio file.

        Returns:
            Optional[BinaryIO]: The opened audio file in binary mode or None if an error occurs.
        """
        try:
            audio_file = open(path, "rb")
            return audio_file
        except Exception as e:
            logger.error(f"Error while opening file: {e}")
            return None

    def transcribe_audio(self, audio_file: BinaryIO, language: str) -> Optional[Transcription]:
        """
        Transcribes the audio file using the specified language and returns the transcription.

        Args:
            audio_file (BinaryIO): The audio file object in binary mode.
            language (str): The language code for transcription.

        Returns:
            Optional[Transcription]: The transcription object or None if an error occurs.
        """
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
            return None

    @staticmethod
    def format_text(transcription: Transcription) -> List[Fragment]:
        """
        Formats the transcription text into fragments with start and end times.

        Args:
            transcription (Transcription): The transcription object.

        Returns:
            List[Fragment]: A list of Fragment objects representing the formatted text.
        """
        fragments = []
        current_fragment = None

        for text in transcription.words:
            if current_fragment is None:
                current_fragment = Fragment(
                    start_time=text.get("start"),
                    end_time=text.get("start") + text.get("end") - text.get("start"),
                    transcriptions=text.get("word")
                )
            else:
                if text.get("word").endswith("."):
                    current_fragment.transcriptions += " " + text.get("word")
                    fragments.append(current_fragment)
                    current_fragment = None
                else:
                    current_fragment.transcriptions += " " + text.get("word")
                    current_fragment.end_time = text.get("start") + text.get("end") - text.get("start")

        if current_fragment is not None:
            fragments.append(current_fragment)

        return fragments

    def transcribe(self, language: str) -> Optional[FragmentList]:
        """
        Transcribes the audio file, formats the text, and returns a list of fragments.

        Args:
            language (str): The language code for transcription.

        Returns:
            Optional[FragmentList]: A FragmentList object containing the list of formatted text fragments.
        """
        audio_file = self.get_audio_file(self.audio_file_path)
        transcription = self.transcribe_audio(audio_file, language)

        if not transcription:
            logger.info(f"Transcription not found for {self.audio_file_path}")
            return None

        logger.info(f"{self.audio_file_path} transcribed successfully")

        formatted_text = self.format_text(transcription)

        logger.info(f"{self.audio_file_path} formatted successfully")

        return FragmentList(type_="LLM", fragments=formatted_text)
