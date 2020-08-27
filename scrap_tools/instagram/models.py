from django.db import models

# Create your models here.

class Instagram(models.Model):

    ig_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    following = models.IntegerField()
    followers = models.IntegerField()
    post_data = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
