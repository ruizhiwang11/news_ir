from unicodedata import category
from django.db import models

# Create your models here.

class News(models.Model):

    category = models.CharField(max_length=20)
    location = models.CharField(max_length=10)
    title = models.CharField(max_length=40, unique=True)
    author = models.CharField(max_length=10)
    created_time = models.DateTimeField()
    content = models.CharField(max_length=10000)
    image = models.CharField(max_length=10000)