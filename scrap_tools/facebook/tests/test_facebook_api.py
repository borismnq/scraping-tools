from django.test import TestCase
from facebook.models import Facebook


class FacebookTests(TestCase):
    """Test Facebook"""

    def setUp(self):
        pass

    def test_model(self):
        """Test model"""
        fb_attached_post = Facebook.objects.create(
            shared="Shared post username",
            shared_id="101010101010",
            original="Original post username",
            original_id="202020202020"
        )

        self.assertEqual(str(fb_attached_post), fb_attached_post.original_id)
