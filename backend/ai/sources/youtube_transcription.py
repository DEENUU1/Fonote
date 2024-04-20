from typing import Optional, List, Dict, Any
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from dataclasses import dataclass


@dataclass
class Fragment:
    start_time: float
    end_time: float
    transcriptions: str


class YoutubeTranscription:
    def __init__(self, url: str):
        self.url = url

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

    def get_youtube_transcription(self, video_id: str, language: str):
        text = None
        type_ = None

        try:
            transcription_list = YouTubeTranscriptApi.list_transcripts(video_id)
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
            return text, type_

        return text, type_

    def format_text(self, full_text: List[Dict[str, Any]]):
        fragments = []
        current_fragment = None

        for text in full_text:
            if current_fragment is None:
                current_fragment = Fragment(start_time=text["start"], end_time=text["start"] + text["duration"],
                                            transcriptions=text["text"])
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






if __name__ == "__main__":
    import json

    url = "https://www.youtube.com/watch?v=39jB8nJBrCI"

    youtube_transcript = YoutubeTranscription(url)
    # video_id = youtube_transcript.get_youtube_video_id(url)
    # transcription = youtube_transcript.get_youtube_transcription(video_id, "English")

    with open("transcription.json", "r") as f:
        transcription = json.load(f)

    formatted_text = youtube_transcript.format_text(transcription)
    print(formatted_text[0])