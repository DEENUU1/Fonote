import base64
import requests
import json
import logging
from django.conf import settings


logger = logging.getLogger(__name__)


class SpotifyAccess:
    def __init__(self):
        self.__client_id: str = settings.SPOTIFY_CLIENT_ID
        self.__client_secret: str = settings.SPOTIFY_CLIENT_SECRET
        self.base_url = "https://accounts.spotify.com/api/token"

    def get_token(self) -> str:
        auth_string = f'{self.__client_id}:{self.__client_secret}'
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}

        try:
            result = requests.post(self.base_url, headers=headers, data=data)
            result.raise_for_status()

            json_result = json.loads(result.content)
            token = json_result["access_token"]
            print(token)
            return token

        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTPError {err}")

        except requests.exceptions.RequestException as err:
            logger.error(f"RequestException {err}")

        except Exception as err:
            logger.error(f"Exception {err}")
