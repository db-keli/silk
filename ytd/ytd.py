from urllib.error import HTTPError
from pytube import Playlist
from pytube import YouTube, Stream
import io
from typing import List, Optional, Tuple
from pytube import request
from fastapi import HTTPException


Buffer = io.BytesIO()


from typing import List


def download_playlist(url, resolution):
    playlist = Playlist(url)
    downloaded_streams = []

    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    for video in playlist.videos:
        stream = video.streams.filter(res=resolution).first()
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
    bytes_remaining = stream.filesize
    try:
        for chunk in request.stream(
            stream.url, timeout=timeout, max_retries=max_retries
        ):
            print(bytes_remaining)
            bytes_remaining -= len(chunk)
            print("here")
            yield chunk
    except HTTPError as e:
        if e.code != 404:
            raise e
        for chunk in request.seq_stream(
            stream.url, timeout=timeout, max_retries=max_retries
        ):
            bytes_remaining -= len(chunk)
            print("there")
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
