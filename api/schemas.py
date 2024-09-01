"""
    This module defines the schemas used for the application.
    
    It includes the following schemas:
    - Video: A schema for the necessary data about the video to be dowloaded.
    - Playlist: A schema for the necessary data about the playlist to be downloaded
"""

from pydantic import BaseModel


class Video(BaseModel):
    """
    Video schema, which contains the URL and resolution of the video to be downloaded.
    Args:
        BaseModel (_type_): _description_
    """

    url: str
    resolution: str


class Playlist(BaseModel):
    """
    Playlist, schema, contains the URL and resolution of the playlist to be downloaded.

    Args:
        BaseModel (_type_): _description_
    """

    url: str
    resolution: str
