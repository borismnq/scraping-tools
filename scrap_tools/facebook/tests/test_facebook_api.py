from django.test import TestCase

from facebook.models import Facebook

from selenium import webdriver
from selenium.webdriver.common.by import By

import os


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


class FacebookSeleniumTests(TestCase):

    def setUp(self):
        self.facebook_url = os.environ.get('FACEBOOK_URL')
        self.fb_email = os.environ.get('FB_EMAIL')
        self.fb_pass = os.environ.get('FB_PASS')

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--incognito')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Remote(
            command_executor='http://hub:4444/wd/hub',
            desired_capabilities={
                    'browserName': 'chrome',
                    'version': '',
                    "chrome.switches": ["disable-web-security"],
                    'platform': 'ANY'
            })

    def test_fb_login_exists(self):
        """Test facebook login page"""
        driver = self.driver
        url = self.facebook_url
        driver.get(url)
        username = driver.find_element(By.ID, "email")
        password = driver.find_element(By.ID, "pass")
        self.assertIsNotNone(username)
        self.assertIsNotNone(password)

    def tearDown(self):
        self.driver.close()
