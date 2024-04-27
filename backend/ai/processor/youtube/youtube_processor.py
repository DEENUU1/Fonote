import logging
from typing import Optional

from ai.models import InputData
from ai.processor.audio.audio_transcript import AudioTranscription
from ai.repositories.fragment_repository import FragmentRepository
from ai.repositories.input_repository import InputDataRepository
from ai.serializers.fragment_serializers import FragmentInputSerializer
from ai.serializers.input_data_serializers import InputDataUpdateSerializer
from .youtube_data import get_youtube_video_data
from .youtube_downloader import YoutubeDownloader
from .youtube_transcription import YoutubeTranscription
from ..audio.fragment_list import FragmentList

logger = logging.getLogger(__name__)


class YoutubeProcessor:
    """
    A class for processing input data from YouTube.

    Attributes:
        input_data (InputData): The input data object to be processed.
        transcription_type (Optional[str]): The type of audio to perform, defaults to None.

    Methods:
        map_languages_to_code(language: str) -> str:
            Maps human-readable language names to their corresponding language codes.
        get_transcription(source_url: str, language: Optional[str] = None) -> Optional[FragmentList]:
            Retrieves the audio of the YouTube video and returns it as a FragmentList object.
        process() -> None:
            Processes the input data, retrieves the audio, and updates the database accordingly.
    """

    def __init__(self, input_data: InputData, transcription_type: Optional[str] = None):
        """
        Initialize YoutubeProcessor instance.

        Args:
            input_data (InputData): The input data object to be processed.
            transcription_type (Optional[str]): The type of audio to perform, defaults to None.
        """
        self.input_repository = InputDataRepository()
        self.fragment_repository = FragmentRepository()
        self.input_data = input_data
        self.transcription_type = transcription_type

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

    def get_transcription(
            self,
            source_url: str,
            language: Optional[str] = None,
    ) -> Optional[FragmentList]:
        """
        Retrieves the audio of the YouTube video and returns it as a FragmentList object.

        Args:
            source_url (str): The URL of the YouTube video.
            language (Optional[str]): The language for audio, defaults to None.

        Returns:
            Optional[FragmentList]: A FragmentList object containing the audio fragments,
                or None if no audio is found.
        """
        if self.transcription_type == "LLM":
            youtube_downloader = YoutubeDownloader(source_url)
            downloaded_video = youtube_downloader.download()

            if not downloaded_video:
                logger.error("Couldn't download youtube video")
                self.input_repository.update_status(self.input_data, "ERROR")
                return

            audio_transcription = AudioTranscription(audio_file_path=downloaded_video)
            lang_code = self.map_languages_to_code(language)
            transcription = audio_transcription.transcribe(lang_code)
            return transcription

        else:
            youtube_transcription = YoutubeTranscription(source_url)
            transcription = youtube_transcription.get_transcription(language)
            return transcription

    def process(self) -> None:
        """
        Processes the input data, retrieves the audio, and updates the database accordingly.
        """
        logger.info(f"Processing input data {self.input_data.id}")

        video_data = get_youtube_video_data(self.input_data.source_url)
        transcription = self.get_transcription(self.input_data.source_url, self.input_data.language)

        if not transcription:
            self.input_repository.update_status(self.input_data, "ERROR")
            return

        data = {
            "transcription_type": transcription.type_,
            "audio_length": video_data.length if video_data else None,
            "source_title": video_data.title if video_data else None,
        }
        input_data_update_serializer = InputDataUpdateSerializer(data=data)
        input_data_update_serializer.is_valid(raise_exception=True)
        self.input_repository.partial_update(input_data_update_serializer.validated_data, self.input_data)

        for idx, fragment in enumerate(transcription.fragments):
            data = {
                "start_time": fragment.start_time,
                "end_time": fragment.end_time,
                "order": idx,
                "text": fragment.transcriptions,
                "input_data": self.input_data.id
            }
            fragment_serializer = FragmentInputSerializer(data=data)
            fragment_serializer.is_valid(raise_exception=True)
            self.fragment_repository.create(fragment_serializer.validated_data)

        logger.info(f"Input data {self.input_data.id} processed")
        self.input_repository.update_status(self.input_data, "DONE")
        return
