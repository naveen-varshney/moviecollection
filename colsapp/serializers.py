from rest_framework import fields, serializers
from .models import MovieCollection, MovieGenre, Movie, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    favourite_genres = serializers.SerializerMethodField()

    class Meta:
        model = MovieCollection
        fields = ("id", "title", "description", "movies", "user", "favourite_genres")

    def get_favourite_genres(self, obj):
        return []

    def create(self, validated_data):
        movies = validated_data.pop("movies")
        collection = MovieCollection.objects.create(**validated_data)

        for movie in movies:
            collection.movies.add(movie)
        return collection

    def update(self, instance, validated_data):
        movies = validated_data.pop("movies")
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        instance.movies.set(movies)
        return instance


class GenresSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = MovieGenre
        fields = ("id", "name")


class MovieSerializer(serializers.ModelSerializer):
    genres = GenresSerializer(many=True)
    collections = serializers.PrimaryKeyRelatedField(
        queryset=MovieCollection.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Movie
        fields = ("id", "title", "description", "collections", "genres")

    def create(self, validated_data):
        collections = validated_data.pop("collections")
        genres = validated_data.pop("genres")
        movie = Movie.objects.create(**validated_data)

        for collection in collections:
            movie.collections.add(collection)

        for gen in genres:
            # creating genre in case of not exists
            genre, status = MovieGenre.objects.get_or_create(
                name=gen["name"].capitalize()
            )
            movie.genres.add(genre)
        return movie
