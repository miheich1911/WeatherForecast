from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class City(models.Model):
    name = models.CharField(max_length=28)
    searcher = models.ManyToManyField(User, blank=True, null=True, related_name='cities')

    def __str__(self):
        return self.name
