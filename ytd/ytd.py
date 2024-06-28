from urllib.error import HTTPError
from pytube import Playlist
from pytube import YouTube, Stream
import io
from typing import List, Optional, Tuple
from pytube import request


Buffer = io.BytesIO()


from typing import List


def download_playlist(url, resolution) -> List[Tuple[YouTube, io.BytesIO]]:
    playlist = Playlist(url)
    downloaded_buffers = []

    for video in playlist.videos:
        stream = video.streams.filter(res=resolution).first()
        stream.stream_to_buffer(Buffer)
        Buffer.seek(0)
        downloaded_buffers.append((video.thumbnail_url, Buffer))
        return downloaded_buffers


def download_video(url, resolution) -> Stream:
    """
    Downloads a video stream from the given URL with the specified resolution.

    Args:
        url (str): The URL of the video.
        resolution: The resolution of the video stream.

    Returns:
        Stream: The downloaded video stream.
    """
    yt = YouTube(url)
    stream = yt.streams.filter(res=resolution).first()
    if not stream:
        return
    else:
        return stream


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
            raise
        for chunk in request.seq_stream(
            stream.url, timeout=timeout, max_retries=max_retries
        ):
            bytes_remaining -= len(chunk)
            print("there")
            yield chunk
