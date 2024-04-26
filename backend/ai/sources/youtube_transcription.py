import logging
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

from .fragment import Fragment
from .fragment_list import FragmentList

logger = logging.getLogger(__name__)


class YoutubeTranscription:
    def __init__(self, url: str):
        self.video_id = self.get_youtube_video_id(url)

    @staticmethod
    def get_youtube_video_id(url: str) -> Optional[str]:
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

    def fetch_transcription(self, language: str):
        text = None
        type_ = None

        try:
            transcription_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
            generated, manually = None, None
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

            if generated:
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
    def format_text(full_text: List[Dict[str, Any]]):
        fragments = []
        current_fragment = None

        for text in full_text:
            if current_fragment is None:
                current_fragment = Fragment(
                    start_time=text["start"],
                    end_time=text["start"] + text["duration"],
                    transcriptions=text["text"]
                )
            else:
                if text["text"].endswith("."):
                    current_fragment.transcriptions += " " + text["text"]
                    fragments.append(current_fragment)
                    current_fragment = None
                else:
                    current_fragment.transcriptions += " " + text["text"]
                    current_fragment.end_time = text["start"] + text["duration"]

        if current_fragment is not None:
            fragments.append(current_fragment)

        return fragments

    def get_transcription(self, language: str) -> Optional[FragmentList]:
        fetched_transcript, type_ = self.fetch_transcription(language)

        if fetched_transcript is None:
            return None

        formatted_text = self.format_text(fetched_transcript)

        return FragmentList(type_, formatted_text)
