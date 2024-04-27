import logging
from typing import Optional, List, Dict, Any, Tuple
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

from ai.processor.transcription.fragment import Fragment
from ai.processor.transcription.fragment_list import FragmentList

logger = logging.getLogger(__name__)


class YoutubeTranscription:
    """
    A class for fetching and formatting transcriptions of YouTube videos.

    Attributes:
        video_id (str): The ID of the YouTube video.

    Methods:
        get_youtube_video_id(url: str) -> Optional[str]:
            Static method to extract the video ID from a YouTube video URL.
        map_languages_to_code(language: str) -> str:
            Maps human-readable language names to their corresponding language codes.
        fetch_transcription(language: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
            Fetches the transcription of the YouTube video in the specified language.
        format_text(full_text: List[Dict[str, Any]]) -> List[Fragment]:
            Formats the transcription text into fragments with start and end times.
        get_transcription(language: str) -> Optional[FragmentList]:
            Gets the transcription of the YouTube video in the specified language as a FragmentList object.
    """

    def __init__(self, url: str):
        """
        Initialize YoutubeTranscription instance.

        Args:
            url (str): The URL of the YouTube video.
        """
        self.video_id = self.get_youtube_video_id(url)

    @staticmethod
    def get_youtube_video_id(url: str) -> Optional[str]:
        """
        Static method to extract the video ID from a YouTube video URL.

        Args:
            url (str): The URL of the YouTube video.

        Returns:
            Optional[str]: The video ID extracted from the URL, or None if extraction fails.
        """
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]

        return None

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

    def fetch_transcription(self, language: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Fetches the transcription of the YouTube video in the specified language.

        Args:
            language (str): The language for transcription.

        Returns:
            Tuple[Optional[List[Dict[str, Any]]], Optional[str]]: A tuple containing the fetched transcription text
                as a list of dictionaries and the type of transcription fetched (either "MANUAL" or "GENERATED").
        """
        text, type_ = None, None
        generated, manually = None, None

        try:
            transcription_list = YouTubeTranscriptApi.list_transcripts(self.video_id)

            if not transcription_list:
                logger.info(f"No transcription found for video {self.video_id}")
                return text, type_

            for transcript in transcription_list:
                if language in transcript.language:
                    if transcript.is_generated:
                        generated = transcript
                    else:
                        manually = transcript

            if not generated and not manually:
                lang_code = self.map_languages_to_code(language)

                for transcript in transcription_list:
                    translation_languages = transcript.translation_languages

                    for lang in translation_languages:
                        if language in lang.get("language"):
                            generated = transcript.translate(lang_code)
                            type_ = "GENERATED"

            if generated and manually:
                text = manually.fetch()
                type_ = "MANUAL"
            elif generated:
                text = generated.fetch()
                type_ = "GENERATED"

        except TranscriptsDisabled:
            logger.error(f"Transcripts disabled for video {self.video_id}")
            return text, type_

        except Exception as e:
            logger.error(e)
            return text, type_

        return text, type_

    @staticmethod
    def format_text(full_text: List[Dict[str, Any]]) -> List[Fragment]:
        """
        Formats the transcription text into fragments with start and end times.

        Args:
            full_text (List[Dict[str, Any]]): The full transcription text as a list of dictionaries.

        Returns:
            List[Fragment]: A list of Fragment objects representing the formatted text.
        """
        fragments = []
        current_fragment = None

        for text in full_text:
            if current_fragment is None:
                current_fragment = Fragment(
                    start_time=text.get("start"),
                    end_time=text.get("start") + text.get("duration"),
                    transcriptions=text.get("text")
                )
            else:
                if text.get("text").endswith("."):
                    current_fragment.transcriptions += " " + text.get("text")
                    fragments.append(current_fragment)
                    current_fragment = None
                else:
                    current_fragment.transcriptions += " " + text.get("text")
                    current_fragment.end_time = text.get("start") + text.get("duration")

        if current_fragment is not None:
            fragments.append(current_fragment)

        return fragments

    def get_transcription(self, language: str) -> Optional[FragmentList]:
        """
        Gets the transcription of the YouTube video in the specified language as a FragmentList object.

        Args:
            language (str): The language for transcription.

        Returns:
            Optional[FragmentList]: A FragmentList object containing the formatted text fragments,
                or None if no transcription is found.
        """
        fetched_transcript, type_ = self.fetch_transcription(language)

        logger.info(f"Transcription type: {type_}")

        if fetched_transcript is None:
            logger.error(f"No transcription found for video {self.video_id}")
            return None

        logger.info(f"Transcription fetched for video {self.video_id}")
        formatted_text = self.format_text(fetched_transcript)

        logger.info(f"Transcription formatted for video {self.video_id}")

        return FragmentList(type_, formatted_text)
