from django.db import models

# Create your models here.

class LoginUser(models.Model):
    username = models.CharField('username',max_length=128)
    password = models.CharField('password',max_length=128)
