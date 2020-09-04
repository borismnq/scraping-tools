from django.test import TestCase

from instagram.models import Instagram

import requests


class InstagramTests(TestCase):
    """Test Instagram"""

    def setUp(self):
        pass

    def test_model(self):
        """Test model"""
        ig_profile = Instagram.objects.create(
            ig_id="646441123", name="claroperu", following=49, followers=90596
        )

        self.assertEqual(str(ig_profile), ig_profile.name)


class InstagramScrapTests(TestCase):
    def setUp(self):
        self.url = "https://www.instagram.com/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64)"
            + " AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu"
            + " Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
        }

    def test_user_profile_data(self):
        """Testing that user profile data page exists"""
        url = self.url + "claroperu/?__a=1"
        headers = self.headers

        response = requests.get(url, headers=headers)
        self.assertIsNotNone(response)
