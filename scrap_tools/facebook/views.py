"""Facebook views"""
# Django
from django.http import HttpResponse
from facebook.models import Facebook
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError

# BeautifulSoup
from bs4 import BeautifulSoup

# Selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Utilities
import json
import time
import re
import os


FACEBOOK_URL = os.environ.get("FACEBOOK_URL")
FB_EMAIL = os.environ.get("FB_EMAIL")
FB_PASS = os.environ.get("FB_PASS")
WEBDRIVER = None


@csrf_exempt
def scrap_attached_posts(request):
    """Scrap facebook attached posts data"""

    id_inserted_list = list()
    WEBDRIVER = create_webdriver()
    status = "OK"
    posts = None
    post_to_save = []
    if WEBDRIVER:
        logged = login_fb(WEBDRIVER)
        if logged:
            scrolled = scroll_custom(2500, WEBDRIVER)
            if scrolled:
                posts = find_posts(WEBDRIVER)

    attached_posts = None
    if posts:
        attached_posts = find_attached_posts(posts)
    else:
        WEBDRIVER.quit()

    if attached_posts:
        for att in attached_posts:
            attached_post = {}

            soup = hover_and_parse(att, WEBDRIVER)

            if soup:

                shared_info = find_who_shared_post(soup)
                if shared_info:
                    attached_post["shared"] = shared_info["who_shared_post"]
                    attached_post["shared_id"] = shared_info["post_id"]

                original_info = find_who_original_post(soup)
                if original_info:
                    attached_post["original"] = original_info["who_original_post"]
                    attached_post["original_id"] = original_info["post_id"]

                post_to_save.append(attached_post)
            else:

                status = "PARSING PROBLEMS"

        # WEBDRIVER.quit()
    else:
        # WEBDRIVER.quit()
        status = "NO ATTACHED POSTS"

    for post in post_to_save:

        try:
            new_post = Facebook.objects.create(**post)
            id_inserted_list.append(new_post.id)

        except IntegrityError as e:
            status = e

    response = {"status": str(status), "facebook_id_inserted": id_inserted_list}

    return HttpResponse(json.dumps(response), content_type="application/json")


def create_webdriver():
    """ Creates a chrome webdriver with custom options"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # options.add_argument("window-size=1400,900")
    options.add_argument("--incognito")
    options.add_argument("--ignore-certificate-errors")
    WEBDRIVER = webdriver.Remote(
        command_executor="http://hub:4444/wd/hub",
        desired_capabilities={
            "browserName": "chrome",
            "version": "",
            "chrome.switches": ["disable-web-security"],
            "platform": "ANY",
        },
    )
    return WEBDRIVER


def login_fb(WEBDRIVER):
    """Login on fb, and waiting for page load"""
    try:
        WEBDRIVER.get(FACEBOOK_URL)

        username = WEBDRIVER.find_element(By.ID, "email")
        password = WEBDRIVER.find_element(By.ID, "pass")

        username.send_keys(FB_EMAIL)
        password.send_keys(FB_PASS)

        WEBDRIVER.find_element(By.ID, "u_0_b").click()

        time.sleep(10)
        return True
    except NoSuchElementException:
        return False


def scroll_custom(pxs, WEBDRIVER):
    """Scrolls custom pixeles and wait 4 secs for loading"""
    try:
        WEBDRIVER.execute_script(f"window.scrollBy(0, {pxs})")
        time.sleep(4)
        return True
    except Exception:
        return False


def find_posts(WEBDRIVER):
    """Returns all posts from facebook feed"""

    try:
        return WEBDRIVER.find_elements_by_xpath(
            "//div[@data-testid='Keycommand_wrapper_feed_story']"
        )
    except NoSuchElementException:
        return None


def find_attached_posts(posts):
    """Returns all attached posts from list of posts"""
    attached_posts = []
    for post in posts:
        try:
            soup = BeautifulSoup(post.get_attribute("innerHTML"), "html.parser")
            if (
                soup.select("div[data-testid*=Keycommand_wrapper_feed_attached_story]")
                != []
            ):
                attached_posts.append(post)
        except NoSuchElementException:
            pass

    return attached_posts


def hover_and_parse(attached_post, WEBDRIVER):
    """Hover in order to load more html components"""
    try:
        div_describedby = attached_post.find_element_by_xpath(
            ".//div[@aria-describedby]"
        )
        classes_group = div_describedby.get_attribute("aria-describedby").split(" ")
        posted_time_pre = attached_post.find_element_by_id(classes_group[0])
        posted_time = posted_time_pre.find_elements_by_xpath("./span")

        for time_obj in posted_time:
            if not time_obj.get_attribute("class"):
                hover = ActionChains(WEBDRIVER).move_to_element(time_obj)
                hover.perform()

        attached_object = attached_post.find_element_by_xpath(
            ".//div[@data-testid='Keycommand_wrapper_feed_attached_story']"
        )
        span = attached_object.find_element_by_xpath(".//span[@aria-labelledby]")
        if span:
            hover = ActionChains(WEBDRIVER).move_to_element(span)
            hover.perform()

        return BeautifulSoup(attached_post.get_attribute("innerHTML"), "html.parser")
    except NoSuchElementException:
        return None


def find_who_shared_post(html):
    """Returns id and name of who shared the post"""
    try:

        aria_labelled_by = html.find("div", {"aria-labelledby": True})
        h4_label = aria_labelled_by.find("h4", id=aria_labelled_by["aria-labelledby"])
        who_shared_post = h4_label.find("span", {"class": None}).string
        post_id = find_post_id(
            aria_labelled_by.find(
                "h4", id=aria_labelled_by["aria-labelledby"]
            ).parent.parent.parent
        )
        return {"who_shared_post": who_shared_post, "post_id": post_id}
    except TypeError:
        return None


def find_who_original_post(html):
    """Returns id and name of who posted original post"""

    try:

        attached_info = html.find(
            "div", {"data-testid": "Keycommand_wrapper_feed_attached_story"}
        )
        who_original_post = ""
        if attached_info.find("strong"):
            who_original_post = attached_info.find("strong").find("span").string
        elif attached_info.select_one("a > span"):
            who_original_post = attached_info.select_one("a > span").string

        post_id = find_post_id(attached_info)

        return {"who_original_post": who_original_post, "post_id": post_id}
    except TypeError:
        return None


def find_post_id(html):
    """Returns post id"""
    try:

        id_list = []
        links = html.find_all("a", href=re.compile("posts"))
        links += html.find_all("a", href=re.compile("photos"))
        links += html.find_all("a", href=re.compile("permalink"))
        links += html.find_all("a", href=re.compile("groups"))

        for link in links:
            fb_id = None
            if "posts" in link["href"]:
                fb_id = link["href"].split("?")[0].split("/")[-1]
            elif "groups" in link["href"] and "permalink" in link["href"]:
                fb_id = link["href"].split("?")[0].split("/")[-2]
            elif "permalink" in link["href"]:
                fb_id = link["href"].split("fbid=")[1].split("&")[0]

            if not fb_id:
                if "photos" in link["href"]:
                    fb_id = link["href"].split("?")[0].split("/")[-2]
                if "videos" in link["href"]:
                    fb_id = link["href"].split("?")[0].split("/")[-2]
            if fb_id:
                id_list.append(fb_id)
        shared_original_ids = []
        for _id in id_list:
            if _id not in shared_original_ids:
                shared_original_ids.append(_id)

        return shared_original_ids[0]
    except TypeError:
        return None
