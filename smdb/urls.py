"""smdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from core import views
from core.views import Register
from smdb import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies', views.Movies.as_view()),
    path('movies/rate', views.RateMovie.as_view()),
    path('movies/<int:pk>', views.MovieDetail.as_view()),
    path('movies/<int:pk>/actors', views.Actors.as_view()),
    path('movies/<int:pk>/directors', views.Directors.as_view()),
    path('login', obtain_auth_token),
    path('register', Register.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)