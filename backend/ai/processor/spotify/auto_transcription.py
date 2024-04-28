import logging
from typing import List, Dict, Optional

import requests
from django.conf import settings

from ai.processor.audio.fragment import Fragment
from ai.processor.audio.fragment_list import FragmentList
from ai.processor.spotify.access import SpotifyAccess

logger = logging.getLogger(__name__)


class SpotifyAutoTranscription:
    def __init__(self, input_url: str):
        self.input_url = input_url
        # self.spotify_access = SpotifyAccess()

        # if not settings.SPOTIFY_CLIENT_TOKEN:
        #     logger.error("Spotify client token is not set")
        #     return
        #
        # if not settings.SPOTIFY_AUTHORIZATION:
        #     logger.error("Spotify authorization is not set")
        #     return

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Accept": "application/json",
            "Accept-Language": "pl",
            "Referer": "https://open.spotify.com/",
            "client-token": "AACebEIdh33w5dB1aas/tgEcFanSoWkPFhZl08VigkC0swdo82/uOONra9FqHSzq2ke+5UyiOcoktfAI0dpJHpe00u41YFUZXGGPLkZVywL/+45uMZluIdnyulBHfd2AHyIcLRNLPgMSRlHxgMvxvuBu+bJj7afMm2xVAVfqQ+bNgCTiKXLFzmTaNr70DiQIu8bxSceeZmL2Y8Q+mH24le4W35Ewjei0Tga4DlIGQaGFnvZR4oBnFbPxa9Us2NqJVf8s4I3VJoI6wYojlZ4rIcTPVBdax8oEWP7McHXQJZ8=",
            "Origin": "https://open.spotify.com",
            "DNT": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "authorization": "Bearer BQCg7WcENa09fg73COdU-jzRgj0-VL5P6CdNZlbiEmv4x4MTwFrweVxbzefsFClfAay-jshr7ufFnlPi1NhELF3l9PXLNcycIyNANSNbA_jZ2o3wvLxnbXGvjJl2ReMFTzCS6kZ2nBNkgco7wSgYZUWkEmBPm12XP1QQIRSzr0CXkSh_p4j0-vRom9y4ISWbmIjKI7DgWy0ZQKQ4T9gElAklk3DdDkG2_WYsvll2ocx0MphMcd33KVJ_ff7sxKy0KV2GC_cAtkKiPVpG8TDu4hsFBwE9waiFakhd-AhBy0Ou6qgo8KfHRQ-KjTSqYU7GkTsvJJT1KzfFCMdecGpat4drX3Hx",
            "Connection": "keep-alive"
        }

    @staticmethod
    def get_transcription_url(input_id: str) -> str:
        return f"https://spclient.wg.spotify.com/transcript-read-along/v2/episode/{input_id}?format=json"

    def get_transcription(self, url: str) -> Optional[Dict]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as err:
            logger.error("HTTP error:", err)
            return

        except requests.exceptions.RequestException as err:
            logger.error("Request exception:", err)
            return

        except Exception as err:
            logger.error("Exception:", err)
            return

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
        logger.info("Run Spotify transcription...")

        episode_id = self.get_episode_id()
        logger.info(f"Episode ID: {episode_id}")

        transcription_url = self.get_transcription_url(episode_id)
        logger.info(f"Transcription URL: {transcription_url}")

        transcription = self.get_transcription(transcription_url)

        if not transcription:
            logger.error("No transcription found")
            return FragmentList(type_="GENERATED", fragments=[])

        formatted_transcription = self.format_transcription(transcription, fragment_duration_sec)
        logger.info("Transcription formatted")

        return FragmentList(type_="GENERATED", fragments=formatted_transcription)
