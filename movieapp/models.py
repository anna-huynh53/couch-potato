from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=140)
    familyName = models.CharField(max_length=140)
    email = models.EmailField()

