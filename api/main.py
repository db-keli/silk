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
