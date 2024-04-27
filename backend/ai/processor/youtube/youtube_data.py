from pytube import YouTube
from typing import Optional
import logging
from .youtube_video_data import YoutubeVideoData


logger = logging.getLogger(__name__)


def get_youtube_video_data(url: str) -> Optional[YoutubeVideoData]:
    """
    Retrieves metadata of a YouTube video.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        Optional[YoutubeVideoData]: An instance of YoutubeVideoData containing metadata of the video,
            or None if an error occurs.
    """
    try:
        yt = YouTube(url)
        return YoutubeVideoData(yt.title, yt.length)
    except Exception as e:
        logger.error(f"Error getting youtube video data: {e}")
        return None
