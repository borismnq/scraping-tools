from django.db import models

# Create your models here.

class Facebook(models.Model):

    shared = models.CharField(max_length=255)
    shared_id = models.CharField(max_length=255)
    original = models.CharField(max_length=255)
    original_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
