from django.db import models

class Anime(models.Model):
    english = models.CharField(max_length=150)
    synonyms = models.CharField(max_length=300)
    japanese = models.CharField(max_length=150)
    kind = models.CharField(max_length=20)
    episodes = models.IntegerField()
    status = models.CharField(max_length=50)
    aired = models.CharField(max_length=50)
    premiered = models.CharField(max_length=50)
    broadcast = models.CharField(max_length=100)
    producers = models.CharField(max_length=500)
    licensors = models.CharField(max_length=100)
    studios = models.CharField(max_length=100)
    source = models.CharField(max_length=50)
    genres = models.CharField(max_length=150)
    duration = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    score = models.DecimalField(max_digits=3, decimal_places=2)
    ranked = models.IntegerField()
    popularity = models.IntegerField()
    members = models.IntegerField()
    favorites = models.IntegerField()
    name = models.CharField(max_length=150)
    description = models.TextField()
    url =  models.CharField(max_length=200)