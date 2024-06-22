from pytube import Playlist 
from pytube import YouTube

def download_playlist(url, resolution):
    """
    Downloads all videos in a playlist from the given URL with the specified resolution.

    Args:
        url (str): The URL of the playlist.
        resolution (str): The desired resolution of the videos to download.

    Returns:
        None

    Raises:
        None
    """
    p = Playlist(url)
    for video in p.videos:
         video.streams.get_by_resolution(resolution).download()

def download_video(url, resolution):
    """
    Downloads a video from the given URL with the specified resolution.

    Parameters:
        url (str): The URL of the video to be downloaded.
        resolution (str): The resolution of the video to be downloaded.

    Returns:
        None
    """
    yt = YouTube(url)
    yt.streams.get_by_resolution(resolution).download()
    print("done")
