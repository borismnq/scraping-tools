from django.test import TestCase
from elpais.models import Elpais


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
