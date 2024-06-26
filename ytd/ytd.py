from pytube import Playlist 
from pytube import YouTube
import io

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
        print(video.streams.get_by_resolution(resolution))

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

# testing buffer
yt = YouTube("https://youtu.be/aID6FoFhZqk?si=HohX-AtO1cEh3rHz")
stream1=yt.streams[0]

# creating buffer
buffer = io.BytesIO()
stream1.stream_to_buffer(buffer)
buffer.seek(0)

# Print buffer details
print(f"Buffer size: {len(buffer.getvalue())} bytes")

if __name__ == "main":

    download_playlist("https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n","720p")