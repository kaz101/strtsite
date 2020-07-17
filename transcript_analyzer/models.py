from django.db import models

# Create your models here.
class Actor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    picture = models.ImageField(blank=True)
class Character(models.Model):
    name = models.CharField(max_length=30)
    picture = models.CharField(max_length=1000)
class Episode(models.Model):
    name = models.CharField(max_length=200)
