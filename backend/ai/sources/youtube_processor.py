from typing import Optional

from .audio_transcript import AudioTranscription
from .youtube_data import get_youtube_video_data
from .youtube_downloader import YoutubeDownloader
from .youtube_transcription import YoutubeTranscription
from ..models import InputData
from ..repositories.input_repository import InputDataRepository
from ..serializers.input_data_serializers import InputDataUpdateSerializer
from ..serializers.fragment_serializers import FragmentInputSerializer
from ..repositories.fragment_repository import FragmentRepository
import logging

logger = logging.getLogger(__name__)


class YoutubeProcessor:
    def __init__(self, input_data: InputData, transcription_type: Optional[str] = None):
        self.input_repository = InputDataRepository()
        self.fragment_repository = FragmentRepository()
        self.input_data = input_data
        self.transcription_type = transcription_type

    @staticmethod
    def map_languages_to_code(language: str) -> str:
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

        youtube_transcription = YoutubeTranscription(self.input_data.source_url)

        transcription = youtube_transcription.get_transcription(self.input_data.language)

        video_data = get_youtube_video_data(self.input_data.source_url)

        if not transcription or self.transcription_type is not None:
            youtube_downloader = YoutubeDownloader(self.input_data.source_url)
            downloaded_video = youtube_downloader.download()

            if not downloaded_video:
                logger.error("Couldn't download youtube video")
                self.input_repository.update_status(self.input_data, "ERROR")
                return

            audio_transcription = AudioTranscription(audio_file_path=downloaded_video)
            lang_code = self.map_languages_to_code(self.input_data.language)
            transcription = audio_transcription.run(lang_code)

            if not transcription:
                logger.error("Couldn't transcribe audio")
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