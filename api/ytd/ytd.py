"""
    This module contains functions for downloading YouTube videos and playlists
"""

import io
from urllib.error import HTTPError
from typing import Optional, Tuple
import asyncio
from pytubefix import Playlist
from pytubefix import YouTube, Stream
from pytubefix import request
from fastapi import HTTPException
from connection_manager import connection_manager  # pylint: disable=import-error

Buffer = io.BytesIO()

request.default_range_size = 85000


def download_playlist(url, resolution, username, loop: asyncio.AbstractEventLoop):
    """
    Downloads a playlist of videos from the given URL with the specified
    resolution and returns a list of tuples, each containing a Stream and
    a tuple of video data.

    Args:
        url (str): The URL of the playlist.
        resolution (str): The desired resolution of the video streams.

    Returns:
        List[Tuple[Stream, Tuple[str, str, str]]]: A list of tuples, each
            containing a Stream and a tuple of video data.

    Raises:
        HTTPException: If the playlist URL is invalid or the playlist is not found.
    """

    playlist = Playlist(url)
    downloaded_streams = []
    asyncio.run_coroutine_threadsafe(
        connection_manager.broadcast(
            data={
                "type": "start-download",
                "video-count": len(playlist.videos),
                "message": f"Downloading playlist: {playlist.title}",
            },
            username=username,
        ),
        loop=loop,
    )
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    for video in playlist.videos:
        stream = video.streams.filter(res=resolution).first()
        data = get_video_data(video)
        asyncio.run_coroutine_threadsafe(
            connection_manager.broadcast(
                data={
                    "type": "progress-check",
                    "message": f"{data[0]} has been downloaded",
                },
                username=username,
            ),
            loop=loop,
        )
        if not stream:
            continue
        downloaded_streams.append((stream, data))
    asyncio.run_coroutine_threadsafe(
        connection_manager.broadcast(
            data={
                "type": "end-download",
                "message": f"Playlist: {playlist.title} has been downloaded",
            },
            username=username,
        ),
        loop=loop,
    )
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
        timeout (Optional[int], optional): The maximum number of seconds to wait for
        each chunk of data. Defaults to None.max_retries (Optional[int], optional):
        The maximum number of times to retry downloading a chunk of data. Defaults to None.

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
    author = yt.author

    return title, picture, author
