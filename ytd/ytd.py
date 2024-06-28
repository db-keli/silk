from pytube import Playlist 
from pytube import YouTube
import io

Buffer = io.BytesIO()
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
    playlist = Playlist(url)
    downloaded_buffers = []
    
    for video in playlist.videos:
        stream = video.streams.filter(res=resolution).first()
        stream.stream_to_buffer(Buffer)
        Buffer.seek(0)
        downloaded_buffers.append((video.title, Buffer))

    print(downloaded_buffers)
    
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
    print("me")
    stream = yt.streams.filter(res=resolution).first()
    if not stream:
        print("none")
        return
    else:
        print("there")
        stream.stream_to_buffer(Buffer)
        Buffer.seek(0)
    return (yt.title, Buffer)

# # testing buffer
# yt = YouTube("https://youtu.be/aID6FoFhZqk?si=HohX-AtO1cEh3rHz")
# stream1=yt.streams[0]

# # creating buffer
# buffer = io.BytesIO()
# stream1.stream_to_buffer(buffer)
# buffer.seek(0)
# # Print buffer details
# print(f"Buffer size: {len(buffer.getvalue())} bytes")


download_video("https://youtu.be/aID6FoFhZqk?si=HohX-AtO1cEh3rHz","360p")