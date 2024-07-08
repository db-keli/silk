from urllib.error import HTTPError
from pytube import Playlist
from pytube import YouTube, Stream
import io
from typing import List, Optional, Tuple
from pytube import request
from fastapi import HTTPException
import concurrent.futures


Buffer = io.BytesIO()

request.default_range_size = 85000

from typing import List

def get_stream(video,resolution):
    stream = video.streams.filter(res=resolution).first()
    return stream, video

def download_playlist(url, resolution):
    playlist = Playlist(url)
    downloaded_streams = []

    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    with concurrent.futures.ThreadPoolExecutor() as executer:
        results = [executer.submit(get_stream,video,resolution) for video in playlist.videos]
        for f in concurrent.futures.as_completed(results):
            stream,video = f.result()
            data = get_video_data(video)
            if not stream:
                continue
            downloaded_streams.append((stream, data))
    return downloaded_streams


def download_video(url, resolution) -> Tuple[Stream, Tuple[str, str, str]]:
    """
    Downloads a video stream from the given URL with the specified resolution.

    Args:
        url (str): The URL of the video.
        resolution: The resolution of the video stream.

    Returns:
        Stream: The downloaded video stream.
    """
    yt = YouTube(url)
    data = get_video_data(yt)
    stream = yt.streams.filter(res=resolution).first()
    if not stream:
        return HTTPException(status_code=404, detail="Video not found")
    else:
        return stream, data


def download(
    stream: Stream, timeout: Optional[int] = None, max_retries: Optional[int] = None
):
    """
    Downloads a video stream from the given Stream object.

    Args:
        stream (Stream): The Stream object representing the video stream to download.
        timeout (Optional[int], optional): The maximum number of seconds to wait for each chunk of data. Defaults to None.
        max_retries (Optional[int], optional): The maximum number of times to retry downloading a chunk of data. Defaults to None.

    Yields:
        bytes: The downloaded chunks of data.

    Raises:
        HTTPError: If an HTTP error occurs and the error code is not 404.

    """
    try:
        for chunk in request.stream(
            stream.url, timeout=timeout, max_retries=max_retries
        ):
            yield chunk
    except HTTPError as e:
        if e.code != 404:
            raise e
        for chunk in request.stream(
                stream.url, timeout=timeout, max_retries=max_retries
        ):
            yield chunk


def get_video_data(yt: YouTube) -> Tuple[str, str, str]:
    """
    A function to retrieve the title, picture, and author of a YouTube video.

    Args:
        yt (YouTube): An instance of the YouTube class containing video information.

    Returns:
        Tuple[str, str, str]: A tuple containing the title, picture URL, and author of the video.
    """
    title = yt.title
    picture = yt.thumbnail_url
    author = yt._author

    return title, picture, author
