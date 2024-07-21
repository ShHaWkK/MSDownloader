import subprocess
import sys
import logging
import yt_dlp
import ffmpeg
import shutil
import os
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {str(e)}")
        sys.exit("Please ensure you have an active internet connection and try again.")

class Downloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s',
            'ffmpeg_location': 'C:/ffmpeg/ffmpeg-7.0.1-essentials_build/bin/ffmpeg.exe'  # Chemin absolu vers ffmpeg
        }

    def download(self, url, platform='YouTube', quality='best'):
        logger.info(f"Attempting to download from {platform}, URL: {url}, Quality: {quality}")
        
        try:
            if quality.lower() == 'best':
                self.ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif quality.lower() in ['1080p', '720p', '480p', '360p']:
                height = quality[:-1]  # Retire le 'p' à la fin
                self.ydl_opts['format'] = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best'
            else:
                logger.warning(f"Unsupported quality: {quality}, defaulting to best")
                self.ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            
            logger.debug(f"yt-dlp options: {self.ydl_opts}")
            logger.debug(f"PATH: {os.environ['PATH']}")

            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
            
            logger.info(f"Download completed: {info['title']}")
            return info['title']
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}", exc_info=True)
            return None

    def get_available_qualities(self, url):
        try:
            with yt_dlp.YoutubeDL({'format': 'bestvideo'}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                qualities = set()
                for f in formats:
                    if f.get('height'):
                        qualities.add(f'{f["height"]}p')
                return sorted(list(qualities), key=lambda x: int(x[:-1]), reverse=True)
        except Exception as e:
            logger.error(f"An error occurred while fetching qualities: {str(e)}", exc_info=True)
            return []

class Converter:
    def __init__(self):
        pass

    def convert_to_mp4(self, input_file, output_file):
        try:
            stream = ffmpeg.input(input_file)
            stream = ffmpeg.output(stream, output_file, vcodec='libx264', acodec='aac')
            ffmpeg.run(stream)
            return True
        except ffmpeg.Error as e:
            logger.error(f"An error occurred during conversion: {str(e)}", exc_info=True)
            return False

class BasePlatform(ABC):
    @abstractmethod
    def get_video_info(self, url):
        pass

    @abstractmethod
    def download(self, url, quality='best'):
        pass

class YouTube(BasePlatform):
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s',
            'ffmpeg_location': 'C:/ffmpeg/ffmpeg-7.0.1-essentials_build/bin/ffmpeg.exe'  # Chemin absolu vers ffmpeg
        }

    def get_video_info(self, url):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def download(self, url, quality='best'):
        self.ydl_opts['format'] = quality
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            return ydl.download([url])

def main():
    install_requirements()

    url = input("Enter the YouTube URL: ")
    quality = input("Enter the desired quality (best, 1080p, 720p, etc.): ")
    downloader = Downloader()
    title = downloader.download(url, quality=quality)
    
    if title:
        print(f"Downloaded video: {title}")
        convert = input("Do you want to convert the video to MP4? (yes/no): ")
        if convert.lower() == 'yes':
            converter = Converter()
            input_file = f"{title}.mp4"
            output_file = f"{title}_converted.mp4"
            if converter.convert_to_mp4(input_file, output_file):
                print(f"Video converted successfully: {output_file}")
            else:
                print("Failed to convert video.")
    else:
        print("Failed to download video.")

if __name__ == "__main__":
    main()
