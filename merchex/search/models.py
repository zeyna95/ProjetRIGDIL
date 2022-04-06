# Create your models here.
from django.contrib.auth.models import AbstractUser , UserManager
from django.db import models
class User(AbstractUser):

    email = models.EmailField(max_length=50)
    pays = models.CharField(max_length=30)
    sexe = models.CharField(max_length=30)
    matrimoniale = models.CharField(max_length=50)
    profession = models.CharField(max_length=100)