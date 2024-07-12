import unittest
from src.downloader import Downloader

class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.downloader = Downloader()

    def test_youtube_download(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = self.downloader.download(url, "YouTube", "720p")
        self.assertIsNotNone(result)

    def test_invalid_url(self):
        url = "https://www.invalid-url.com/video"
        result = self.downloader.download(url, "YouTube", "best")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
