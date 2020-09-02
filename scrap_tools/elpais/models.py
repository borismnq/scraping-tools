from django.db import models


class Elpais(models.Model):

    url = models.CharField(max_length=255)
    publish_date = models.DateTimeField(max_length=255)
    title = models.CharField(max_length=255)
    text = models.TextField(default="")
    video = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
