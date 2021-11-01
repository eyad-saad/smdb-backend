from django.contrib import admin

# Register your models here.
from .models import Movie, Actor, Director, UserMovie, Genre

admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(UserMovie)
admin.site.register(Genre)
