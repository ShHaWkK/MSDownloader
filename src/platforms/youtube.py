import yt_dlp
from .base import BasePlatform

class YouTube(BasePlatform):
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s'
        }

    def get_video_info(self, url):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def download(self, url, quality='best'):
        self.ydl_opts['format'] = quality
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            return ydl.download([url])
