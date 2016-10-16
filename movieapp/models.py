import datetime
from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class Friendship(models.Model):
    to_user = models.ForeignKey(User, related_name="friends")
    from_user = models.ForeignKey(User, related_name="_unused_")
    added = models.DateField(default=datetime.date.today)
    
    class Meta:
        unique_together = (('to_user', 'from_user'),)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    watchedList = models.ManyToManyField(Movie, blank=True, related_name='watched')
    toWatchList = models.ManyToManyField(Movie, blank=True, related_name='toWatch')
    friends = models.ManyToManyField(Friendship, blank=True)


# create profile after a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Genre(models.Model):
    name = models.CharField(max_length=100)
    tmdbID = models.CharField(max_length=5)

    def __str__(self):
        return self.name