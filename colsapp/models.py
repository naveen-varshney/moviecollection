import uuid
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class MovieGenre(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        app_label = "colsapp"

    def __str__(self):
        return f"Genre Name : {self.name}"


class MovieCollection(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")

    class Meta:
        verbose_name = "Movie Collection"
        verbose_name_plural = "Movie Collections"
        app_label = "colsapp"

    def __str__(self):
        return f"Name : {self.title}"

    @staticmethod
    def fav_genres(user):
        fav_genres = (
            MovieGenre.objects.filter(movies__collections__user=user)
            .values_list("name", flat=True)
            .annotate(movie_count=Count("movies"))
            .order_by("-movie_count")[:3]
        )
        return list(fav_genres)


class Movie(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    collections = models.ManyToManyField(MovieCollection, related_name="movies",)
    genres = models.ManyToManyField(MovieGenre, related_name="movies")

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        app_label = "colsapp"

    def __str__(self):
        return f"Name : {self.title}"
