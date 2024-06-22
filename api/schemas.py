from pydantic import BaseModel

class Video(BaseModel):
    url: str
    resolution: str