from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import Playlist, Video
import os
import sys
import mimetypes
from dotenv import load_dotenv

load_dotenv()
repository_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, repository_path)

from ytd import ytd

app = FastAPI()
frontend_host = os.getenv("FRONTEND_HOST")


origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/download-video")
async def single_video_download(video: Video):
    """
    Downloads a video from the given URL with the specified resolution and returns a streaming response.

    Parameters:
        video (Video): The video object containing the URL and resolution of the video to be downloaded.

    Returns:
        StreamingResponse: The streaming response containing the downloaded video.

    Raises:
        None.

    Example Usage:
        video = Video(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", resolution="720p")
        response = await single_video_download(video)
    """
    url = video.url
    resolution = video.resolution

    youtubeVideo = ytd.download_video(url, resolution)
    title = youtubeVideo[1][0]
    video_stream = youtubeVideo[0]
    media_type, _ = mimetypes.guess_type(title)

    return StreamingResponse(
        ytd.download(video_stream, timeout=1000, max_retries=6),
        media_type=media_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{title}.mp4"'},
    )


@app.get("/download-video")
async def get_video_data(url: str, resolution: str):
    """
    Retrieves video data from the specified URL and resolution.

    Args:
        url (str): The URL of the video.
        resolution (str): The desired resolution of the video.

    Returns:
        dict: A dictionary containing the video data.

    Raises:
        None.

    Example Usage:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        resolution = "720p"
        video_data = await get_video_data(url, resolution)
        print(video_data)
    """
    youtubeVideo = ytd.download_video(url, resolution)
    data = youtubeVideo[1]
    return {"data": data}


@app.post("/download-playlist")
async def stream_video(playlist: Playlist):
    """
    Downloads a playlist of videos from the given URL with the specified video resolution and returns a streaming response for each video.

    Parameters:
        playlist (Playlist): The playlist object containing the URL and video resolution of the playlist to be downloaded.

    Yields:
        StreamingResponse: A streaming response containing the downloaded video for each video in the playlist.

    Raises:
        None.

    Example Usage:
        playlist = Playlist(url="https://www.youtube.com/playlist?list=PL3nQyYezyvZQ8N-h7Qkz46o5q5jYl0mOj", resolution="720p")
        for response in stream_video(playlist):
            # handle each streaming response
    """
    url = playlist.url
    video_resolution = playlist.resolution

    youtube_videos = ytd.download_playlist(url, video_resolution)

    for video, i in (youtube_videos, range(0, len(youtube_videos))):
        title = video[i].title
        media_type, _ = mimetypes.guess_type(title)

        yield StreamingResponse(
            ytd.download(video[i], timeout=1000, max_retries=6),
            media_type=media_type or "application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{title}.mp4"'},
        )
