from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status

# Create your views here.
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Movie, UserMovie
from core.serializers import MovieSerialzier, RatingSerializer, UserSerializer, ActorSerializer, DirectorSerializer, BuyMovieSerializer


class Movies(APIView):
    def get(self, request):
        filter_term = request.GET.get('filter')
        if filter_term:
            movies = Movie.objects.filter(title__startswith=filter_term)
        else:
            movies = Movie.objects.all()

        search_term = request.GET.get('search-term')
        if search_term:
            movies = movies.filter(Q(actors__name__startswith=search_term)
                                          | Q(directors__name__startswith=search_term)
                                          | Q(title__startswith=search_term)
                                          | Q(genres__name__startswith=search_term)

                                          )

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(movies, request)

        serializer = MovieSerialzier(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MovieDetail(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerialzier(movie)
        return Response(serializer.data)


class Actors(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        actors = movie.actors
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)


class Directors(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        actors = movie.actors
        serializer = DirectorSerializer(actors, many=True)
        return Response(serializer.data)


class RateMovie(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.validated_data['rating']
        movie = serializer.validated_data['movie']
        user_movie_object = UserMovie.objects.filter(user=user, movie=movie)
        if user_movie_object:
            user_movie_object[0].rating = rating
            user_movie_object[0].save()
        else:
             UserMovie.objects.create(user=user, movie=movie, rating=rating)
        return Response(data={'success'})


class Register(CreateAPIView):
    model = User
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserSerializer


class BuyMovie(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        movie = Movie.objects.get(pk=pk)
        serializer = BuyMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_movie_object = UserMovie.objects.filter(user=user, movie=movie)
        if not user_movie_object:
            UserMovie.objects.create(user=user, movie=movie, bought=True)
        if user_movie_object and user_movie_object[0].bought is True:
            raise APIException("already bought")
        if user_movie_object:
            user_movie_object[0].bought = True
            user_movie_object[0].save()
        return Response({'detail': 'success'}, status=status.HTTP_200_OK)
