from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import ManyToManyField


# class Costumer(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    backdrop = models.ImageField(blank=True)
    actors = models.ManyToManyField('core.Actor',  blank=True)
    directors = models.ManyToManyField('core.Director', blank=True)
    user_ratings = models.ManyToManyField('auth.User', blank=True, through='core.UserMovie')
    overview = models.TextField()
    genres = models.ManyToManyField('core.Genre', blank=True)


class Actor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    # movies = ManyToManyField(Movie, null=True, blank=True)


class Director(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(blank=True)

    # movies = ManyToManyField(Movie, null=True, blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=30)


class UserMovie(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movie = models.ForeignKey('core.Movie', on_delete=models.CASCADE)
    rating = models.FloatField(max_length=5)