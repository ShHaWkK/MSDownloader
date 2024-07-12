import yt_dlp
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Downloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s'
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
