from pytube import YouTube
from typing import Optional
from dataclasses import dataclass


@dataclass
class YoutubeVideoData:
    title: str
    length: int


def get_youtube_video_data(url: str) -> Optional[YoutubeVideoData]:
    try:
        yt = YouTube(url)
        title = yt.title
        length = yt.length

        return YoutubeVideoData(title, length)
    except Exception as e:
        # TODO add logger
        print(e)
        return None

