from fastapi import FastAPI
from ytd import ytd
from schemas import Video

app = FastAPI()

app.get('/')
def boilerplate():
    return 'boilerplate'


app.post('/download')
def single_video_download(video: Video):
    
    ytd.download_video