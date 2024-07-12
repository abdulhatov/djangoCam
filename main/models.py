from django.db import models

class Stream(models.Model):
    name = models.CharField(max_length=100)
    source_url = models.CharField(max_length=255)
    destination_url = models.CharField(max_length=255)