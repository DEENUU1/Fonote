from pytube import YouTube
import os
from typing import Optional
import logging
from django.conf import settings


logger = logging.getLogger(__name__)


class YoutubeDownloader:
    def __init__(self, url: str):
        self.url = url

    def download(self) -> Optional[str]:
        try:
            youtube = YouTube(self.url)
            audio_download = youtube.streams.filter(only_audio=True).first()
            out_file = audio_download.download(output_path=settings.DOWNLOADED_MEDIA)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            return new_file
        except Exception as e:
            logger.error(e)
            return
