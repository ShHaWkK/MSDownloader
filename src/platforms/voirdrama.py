import requests
from bs4 import BeautifulSoup
from .base import BasePlatform

class VoirDrama(BasePlatform):
    def get_video_info(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='title').text
        return {'title': title, 'url': url}

    def download(self, url, quality='best'):
        # Implémentez la logique de téléchargement spécifique à VoirDrama
        pass
