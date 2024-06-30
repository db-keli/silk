from pydantic import BaseModel


class Video(BaseModel):
    url: str
    resolution: str


class Playlist(BaseModel):
    url: str
    resolution: str
