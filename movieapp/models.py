from django.db import models

class Movie(models.Model):
    imdbID = models.CharField(max_length=100)
    title = models.CharField(max_length=700)
    year = models.CharField(max_length=100)
    rated = models.CharField(max_length=100)
    released = models.CharField(max_length=100)
    runtime = models.CharField(max_length=100)
    genre = models.CharField(max_length=250)
    director = models.CharField(max_length=400)
    writer = models.CharField(max_length=400)
    actors = models.CharField(max_length=600)
    plot = models.TextField()
    language = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    poster = models.CharField(max_length=1000)
    metascore = models.CharField(max_length=50)
    imdbRating = models.CharField(max_length=50)




class User(models.Model):
    firstName = models.CharField(max_length=200)
    familyName = models.CharField(max_length=200)
    email = models.EmailField()
    watchedList = models.ManyToManyField(Movie)
