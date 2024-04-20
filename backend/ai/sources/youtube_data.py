from pytube import YouTube
from typing import Dict, Any


def get_youtube_video_data(url: str) -> Dict[str, Any]:
    yt = YouTube(url)

    title = yt.title
    length = yt.length

    return {
        "title": title,
        "length": length
    }
