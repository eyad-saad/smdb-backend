from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.authtoken.models import Token

from core.models import UserMovie, Actor, Director, Genre, Costumer


class ActorSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'image']


class DirectorSerializer(ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BuyMovieSerializer(Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    credit_card = serializers.CharField()

    class Meta:
        fields = ['first_name', 'last_name', 'email', 'credit_card']


class MovieSerialzier(Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    image = serializers.ImageField()
    backdrop = serializers.ImageField()
    overview = serializers.CharField()
    actors = ActorSerializer(many=True)
    directors = DirectorSerializer(many=True)
    genres = GenreSerializer(many=True)
    average_rating = SerializerMethodField()
    price = serializers.IntegerField()

    def get_average_rating(self, obj):
        return UserMovie.objects.filter(movie=obj).aggregate(Avg('rating'))['rating__avg']

    class Meta:
        fields = ['id', 'title', 'image', 'backdrop', 'overview', 'actors', 'directors, genres', 'price']


class RatingSerializer(ModelSerializer):
    class Meta:
        model = UserMovie
        fields = ['rating', 'movie']


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    date_of_birth = serializers.DateField(write_only=True)
    marital_status= serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        costumer = Costumer.objects.create(user=user, date_of_birth=validated_data['date_of_birth'],
                                           marital_status=validated_data['marital_status'])
        return user

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return str(token)

    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", "token", "date_of_birth", "marital_status", "email" )

