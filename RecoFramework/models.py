from django.db import models


#python manage.py makemigrations
#python manage.py migrate

class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    age = models.IntegerField()