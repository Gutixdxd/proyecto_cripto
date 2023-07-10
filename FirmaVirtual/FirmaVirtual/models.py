from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    key = models.IntegerField()

class Document():
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sign = models.IntegerField()