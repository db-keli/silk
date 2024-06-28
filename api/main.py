from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from schemas import Video
import os
import sys
import mimetypes
from pytube import YouTube
import io


repository_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, repository_path)

from ytd import ytd

app = FastAPI()


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
    title = youtubeVideo.title

    media_type, _ = mimetypes.guess_type(title)

    return StreamingResponse(
        ytd.download(youtubeVideo, timeout=1000, max_retries=6),
        media_type=media_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{title}.mp4"'},
    )


@app.get("/stream_video/")
async def stream_video(url: str, resolution: str = Query(...)):
    pass
