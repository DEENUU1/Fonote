from .episode import EpisodeData
import logging
from .access import SpotifyAccess
import requests


logger = logging.getLogger(__name__)


class SpotifyAPIWrapper:
    def __init__(self):
        self.spotify_access = SpotifyAccess()

    def _get_token(self) -> str:
        return self.spotify_access.get_token()

    @staticmethod
    def convert_milliseconds_to_seconds(ms: int) -> int:
        return int(ms // 1000)

    def get_episode_data(self, episode_id: str) -> EpisodeData:
        try:
            response = requests.get(
                f"https://api.spotify.com/v1/episodes/{episode_id}",
                headers={
                    "authorization": "Bearer " + self._get_token()
                }
            )
            response.raise_for_status()
            json_result = response.json()

            title = json_result["name"]
            duration_ms = json_result["duration_ms"]
            language = json_result["language"]
            duration_seconds = self.convert_milliseconds_to_seconds(duration_ms)

            return EpisodeData(title=title, duration=duration_seconds, language=language)

        except Exception as e:
            logger.error(e)
