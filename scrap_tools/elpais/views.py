"""Elpais views"""
# Django
from django.http import JsonResponse
from elpais.models import Elpais
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError

# BeautifulSoup
from bs4 import BeautifulSoup

# Utilities
import json
import requests
import os


ELPAIS_URL = os.environ.get("ELPAIS_URL")
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    + "(KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 "
    + "Safari/537.36"
}


@csrf_exempt
def scrap_news(request):
    """Scrap video articles from elpais españa version """
    news_url = _get_video_news()

    video_articles = []
    id_inserted_list = []
    status = "OK"
    if news_url:
        video_articles = [
            _get_article_data(link) for link in news_url if _get_article_data(link)
        ]

    for article in video_articles:
        try:
            new_article = Elpais.objects.create(**article)
            id_inserted_list.append(new_article.id)

        except IntegrityError as e:
            status = e

    response = {"status": str(status), "article_id_inserted": id_inserted_list}

    return JsonResponse(response)


def _download_file(video_objects):
    """Download video if exists save it in a file then returns path"""
    path = "./"
    for video_object in video_objects:
        if "contentUrl" in video_object.keys() and video_object["contentUrl"] != "":

            url = video_object["contentUrl"]
            filename = url.split("/")[-1]
            r = requests.get(url, stream=True)

            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            path += filename
    return path


def _get_article_data(url):
    """ Scrap article data from video~article and returns it"""
    article_data = {}

    response = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(response.text, "html.parser")
    script_tags = soup.find_all("script", type="application/ld+json")
    for script in script_tags:
        if '"@type":"NewsArticle"' in script.string:
            article_object = json.loads(script.string)
            article_data["url"] = article_object.get("url")
            article_data["publish_date"] = article_object.get("datePublished")
            article_data["title"] = article_object.get("headline")
            article_data["text"] = article_object.get("articleBody")
            article_data["video"] = _download_file(article_object["video"])
            break

    return article_data


def _get_video_news():
    """Scrap video~articles urls from elpais (España) and return them"""

    elpais_href_list = []

    response = requests.get(ELPAIS_URL + "/s/setEspana.html", headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    script_tags = soup.find_all("script", type="application/ld+json")

    for script in script_tags:
        if '"@type":"VideoObject"' in script.string:
            article_object = json.loads(script.string)
            elpais_href_list.append(article_object.get("url"))

    return elpais_href_list
