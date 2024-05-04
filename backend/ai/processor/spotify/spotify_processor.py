import logging
from typing import Optional

from ai.models import InputData
from ai.processor.llm.deepl import Translator
from ai.repositories.fragment_repository import FragmentRepository
from ai.repositories.input_repository import InputDataRepository
from ai.serializers.fragment_serializers import FragmentInputSerializer
from ai.serializers.input_data_serializers import InputDataUpdateSerializer
from .api_wrapper import SpotifyAPIWrapper
from ..audio.fragment_list import FragmentList
from .generated_transcription import SpotifyGeneratedTranscription

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

        generated_transcription = SpotifyGeneratedTranscription(source_url)

        return generated_transcription.run()

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
            "English": "en-us",
            "German": "de",
            "French": "fr",
            "Italian": "it",
            "Japanese": "ja",
            "Korean": "ko",
            "Polish": "pl",
            "Spanish": "es",
        }
        return mapper[language]

    @staticmethod
    def get_episode_id(url: str) -> str:
        return url.split("/")[-1]

    def process(self) -> None:
        logger.info(f"Processing input data {self.input_data.id}")

        # api_wrapper = SpotifyAPIWrapper()
        # spotify_data = api_wrapper.get_episode_data(self.get_episode_id(self.input_data.source_url))
        transcription = self.get_transcription(self.input_data.source_url)
        # origin_language_code = spotify_data.language

        lang_code = self.map_languages_to_code(self.input_data.language)

        data = {
            "transcription_type": transcription.type_,
            "audio_length": 69, #spotify_data.duration,
            "source_title": "title", #spotify_data.title
        }

        input_data_update_serializer = InputDataUpdateSerializer(data=data)
        input_data_update_serializer.is_valid(raise_exception=True)
        self.input_repository.partial_update(input_data_update_serializer.validated_data, self.input_data)

        for idx, fragment in enumerate(transcription.fragments):
            transcription_to_save = None

            # if origin_language_code != lang_code:
            #     logger.info(f"Translate from {origin_language_code} to {lang_code}")
            #     translator = Translator(lang_code)
            #     translated_text = translator.translate(fragment.transcriptions)
            #
            #     transcription_to_save = translated_text
            # else:
            transcription_to_save = fragment.transcriptions

            data = {
                "start_time": fragment.start_time,
                "end_time": fragment.end_time,
                "order": idx,
                "text": transcription_to_save,
                "input_data": self.input_data.id
            }
            fragment_serializer = FragmentInputSerializer(data=data)
            fragment_serializer.is_valid(raise_exception=True)
            self.fragment_repository.create(fragment_serializer.validated_data)

        logger.info(f"Input data {self.input_data.id} processed")
        self.input_repository.update_status(self.input_data, "DONE")
        return
