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
            ig_id="646441123",
            name="claroperu",
            following=49,
            followers=90596
        )

        self.assertEqual(str(ig_profile), ig_profile.name)

    def test_user_profile_data(self):
        """Testing user profile data current json structure"""
        url = "https://www.instagram.com/claroperu/?__a=1"

        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64)" +
            " AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu" +
            " Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response = response.json()
        self.assertIsNotNone(response['graphql']['user'])
