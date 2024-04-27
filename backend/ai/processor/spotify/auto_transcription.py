import logging
from typing import List, Dict

import requests

from ai.processor.audio.fragment import Fragment
from ai.processor.audio.fragment_list import FragmentList
from django.conf import settings


logger = logging.getLogger(__name__)


class SpotifyAutoTranscription:
    def __init__(self, input_url: str):
        self.input_url = input_url
        self.headers = {
            "Host": "spclient.wg.spotify.com",
            "client-token": settings.SPOTIFY_CLIENT_TOKEN,
            "authorization": settings.SPOTIFY_AUTHORIZATION,
        }

    @staticmethod
    def get_transcription_url(input_id: str) -> str:
        return f"https://spclient.wg.spotify.com/transcript-read-along/v2/episode/{input_id}?format=json"

    def get_transcription(self, url: str) -> Dict:
        try:

            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as err:
            logger.error("HTTP error:", err)

        except requests.exceptions.RequestException as err:
            logger.error("Request exception:", err)

        except Exception as err:
            logger.error("Exception:", err)

    def get_episode_id(self):
        return self.input_url.split("/")[-1]

    @staticmethod
    def format_transcription(data, fragment_duration_sec=180) -> List[Fragment]:
        fragments = []
        current_start_time = None
        current_transcriptions = []

        for section in data['section']:
            if 'startMs' in section:
                if current_start_time is None:
                    current_start_time = section['startMs'] / 1000
                elif section['startMs'] / 1000 - current_start_time > fragment_duration_sec:
                    fragments.append(Fragment(
                        start_time=current_start_time,
                        end_time=(section['startMs'] - 1) / 1000,
                        transcriptions=" ".join(current_transcriptions)
                    ))
                    current_transcriptions = []
                    current_start_time = section['startMs'] / 1000

            if 'text' in section:
                current_transcriptions.append(section['text']['sentence']['text'])

        if current_start_time is not None:
            fragments.append(Fragment(
                start_time=current_start_time,
                end_time=current_start_time + fragment_duration_sec,
                transcriptions=" ".join(current_transcriptions)
            ))

        return fragments

    def transcribe(self, fragment_duration_sec=180) -> FragmentList:
        episode_id = self.get_episode_id()
        transcription_url = self.get_transcription_url(episode_id)

        transcription = self.get_transcription(transcription_url)

        formatted_transcription = self.format_transcription(transcription, fragment_duration_sec)

        return FragmentList(type_="GENERATED", fragments=formatted_transcription)

