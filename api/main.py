import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ConnectionManager import connection_manager
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
    frontend_host,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loop = asyncio.get_running_loop()

@app.websocket("/{username}")
async def websocket_endpoint(username:str,websocket: WebSocket):
    await connection_manager.connect(websocket,username)
    try:
        while True:
            data = await websocket.receive_json()
            await connection_manager.broadcast(data=data,username=username)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket,username)

@app.post("/download-video")
def single_video_download(video: Video):
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
        headers={"Content-Disposition": f'attachment; filename="{title}.mp4"',
                 "Content-Length":str(video_stream.filesize)},
    )


@app.get("/download-video")
def get_video_data(url: str, resolution: str):
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


def stream_multiple_videos(youtube_videos):
    for video, data in youtube_videos:
        title = video.title
        media_type, _ = mimetypes.guess_type(title)
        yield from ytd.download(video, timeout=1000, max_retries=6)
        yield b"\n\n\n\n\n\n\n" # eof

@app.post("/download-playlist")
def stream_video(playlist: Playlist):
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
    username = playlist.username
    youtube_videos = ytd.download_playlist(url, video_resolution, username, loop)
    content_length = 0
    for video, data in youtube_videos:
        content_length += video.filesize + len(b"\n\n\n\n\n\n\n")
    return StreamingResponse(
        stream_multiple_videos(youtube_videos),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filenames="playlist"',
                 "Content-Length": str(content_length)},
    )
