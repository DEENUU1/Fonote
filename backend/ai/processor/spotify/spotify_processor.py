import logging
from typing import Optional

from ai.models import InputData
from ai.repositories.fragment_repository import FragmentRepository
from ai.repositories.input_repository import InputDataRepository
from ai.serializers.fragment_serializers import FragmentInputSerializer
from ai.serializers.input_data_serializers import InputDataUpdateSerializer
from .auto_transcription import SpotifyAutoTranscription
from ..audio.fragment_list import FragmentList
from ai.processor.llm.deepl import Translator


logger = logging.getLogger(__name__)


class SpotifyProcessor:
    def __init__(self, input_data: InputData, transcription_type: Optional[str] = None):
        self.input_repository = InputDataRepository()
        self.fragment_repository = FragmentRepository()
        self.input_data = input_data
        self.transcription_type = transcription_type

    def get_transcription(self, source_url: str) -> Optional[FragmentList]:

        if self.transcription_type == "LLM":
            raise ValueError("LLM transcription is not supported for Spotify")

        auto_transcription = SpotifyAutoTranscription(source_url)
        transcription = auto_transcription.transcribe()

        return transcription

    @staticmethod
    def map_languages_to_code(language: str) -> str:
        """
        Maps human-readable language names to their corresponding language codes.

        Args:
            language (str): The human-readable language name.

        Returns:
            str: The corresponding language code.
        """
        mapper = {
            "Danish": "da",
            "Czech": "cs",
            "Dutch": "nl",
            "English": "en",
            "German": "de",
            "French": "fr",
            "Italian": "it",
            "Japanese": "ja",
            "Korean": "ko",
            "Polish": "pl",
            "Spanish": "es",
        }
        return mapper[language]

    def process(self) -> None:
        logger.info(f"Processing input data {self.input_data.id}")

        spotify_data = ...  # TODO add this later
        transcription = self.get_transcription(self.input_data.source_url)

        lang_code = self.map_languages_to_code(self.input_data.language)
        translator = Translator(lang_code)

        data = {
            "transcription_type": transcription.type_,
            "audio_length": 69.00,
            "source_title": "Test"
        }

        input_data_update_serializer = InputDataUpdateSerializer(data=data)
        input_data_update_serializer.is_valid(raise_exception=True)
        self.input_repository.partial_update(input_data_update_serializer.validated_data, self.input_data)

        for idx, fragment in enumerate(transcription.fragments):
            translated_text = translator.translate(fragment.transcriptions)

            data = {
                "start_time": fragment.start_time,
                "end_time": fragment.end_time,
                "order": idx,
                "text": translated_text,
                "input_data": self.input_data.id
            }
            fragment_serializer = FragmentInputSerializer(data=data)
            fragment_serializer.is_valid(raise_exception=True)
            self.fragment_repository.create(fragment_serializer.validated_data)

        logger.info(f"Input data {self.input_data.id} processed")
        self.input_repository.update_status(self.input_data, "DONE")
        return
