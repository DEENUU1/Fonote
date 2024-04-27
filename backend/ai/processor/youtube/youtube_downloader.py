import logging
import os
from typing import Optional

from django.conf import settings
from pytube import YouTube

from utils.get_date_hash import get_date_hash

logger = logging.getLogger(__name__)


class YoutubeDownloader:
    """
    A class for downloading audio from YouTube videos.

    Attributes:
        url (str): The URL of the YouTube video.
        format_file (str): The desired file format for downloaded audio, defaults to ".mp3".

    Methods:
        download() -> Optional[str]:
            Downloads the audio from the YouTube video and returns the path to the downloaded file.
    """

    def __init__(self, url: str, format_file: str = ".mp3"):
        """
        Initialize YoutubeDownloader instance.

        Args:
            url (str): The URL of the YouTube video.
            format_file (str): The desired file format for downloaded audio, defaults to ".mp3".
        """
        self.url = url
        self.format_file = format_file

    def download(self) -> Optional[str]:
        """
        Downloads the audio from the YouTube video and returns the path to the downloaded file.

        Returns:
            Optional[str]: The path to the downloaded audio file or None if an error occurs.
        """
        try:
            youtube = YouTube(self.url)
            audio_download = youtube.streams.filter(only_audio=True).first()
            out_file = audio_download.download(output_path=settings.DOWNLOADED_MEDIA)

            new_file_name = get_date_hash() + self.format_file
            new_file_path = os.path.join(settings.DOWNLOADED_MEDIA, new_file_name)
            os.rename(out_file, new_file_path)
            return new_file_path
        except Exception as e:
            logger.error(e)
            return None
