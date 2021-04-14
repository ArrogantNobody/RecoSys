from django.db import models


#python manage.py makemigrations
#python manage.py migrate

class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    age = models.IntegerField()

class Ratings(models.Model):
    userId = models.IntegerField()
    movieId = models.IntegerField()
    rating = models.FloatField()

class Movies(models.Model):
    movieId = models.IntegerField(primary_key=True)
    imdbId = models.IntegerField()
    title = models.CharField(max_length=140)