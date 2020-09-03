from django.test import TestCase
from elpais.models import Elpais

from bs4 import BeautifulSoup

import requests
import json
import os


class ElpaisTests(TestCase):
    """Test Elpais"""

    def setUp(self):
        pass

    def test_model(self):
        """Test model"""
        video_article = Elpais.objects.create(
            url="https://elpais.com/espana/madrid/2020-08-19/noticia.html",
            publish_date="2020-06-09T08:04:22Z",
            title="Noticia title",
            text="Noticia respective content",
            video="media/video.mp4"
        )

        self.assertEqual(str(video_article), video_article.title)


class ElpaisScrapTests(TestCase):

    def setUp(self):
        self.url = os.environ.get('ELPAIS_URL')
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu " +
            "Chromium/71.0.3578.80 Chrome/71.0.3578.80 " +
            "Safari/537.36"
        }

    def test_video_articles(self):
        """Test not empty video article objects """
        url = self.url
        headers = self.headers
        response = requests.get(url+'/s/setEspana.html', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', type="application/ld+json")

        self.assertIsNotNone(script_tags)

        urls = [
            json.loads(script.string).get('url')
            for script in script_tags
            if '"@type":"VideoObject"' in script.string
        ]

        self.assertIsNotNone(urls)
