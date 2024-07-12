from abc import ABC, abstractmethod

class BasePlatform(ABC):
    @abstractmethod
    def get_video_info(self, url):
        pass

    @abstractmethod
    def download(self, url, quality='best'):
        pass
