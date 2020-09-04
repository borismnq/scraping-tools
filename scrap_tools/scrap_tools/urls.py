"""scrap_tools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from instagram import views as instagram_views
from elpais import views as elpais_views
from facebook import views as facebook_views


urlpatterns = [
    path("api/instagram/", instagram_views.scrap_profile, name="scrap_profile"),
    path("api/elpais/", elpais_views.scrap_news, name="scrap_news"),
    path(
        "api/facebook/",
        facebook_views.scrap_attached_posts,
        name="scrap_attached_posts",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
