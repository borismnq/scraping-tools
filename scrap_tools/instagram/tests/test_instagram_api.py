from django.test import TestCase
from instagram.models import Instagram


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
