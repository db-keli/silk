from pytube import Playlist 
from pytube import YouTube




def download_playlist():
    playlist_url = input("Enter playlist  url: ")
    resolution =input("Enter preferred resolution eg.1080p : ")
    p = Playlist(playlist_url)
    for video in p.videos:
         video.streams.get_by_resolution(resolution).download()

def download_video():
    video_url = input("Enter video url: ")
    resolution =input("Enter preferred resolution eg.1080p : ")
    yt = YouTube(video_url)
    yt.streams.get_by_resolution(resolution).download()
    print("done")
