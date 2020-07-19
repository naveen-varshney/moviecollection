import logging
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from maya_api.client import MayaApiClient
from .serializers import MovieSerializer, CollectionSerializer, UserSerializer
from .models import Movie, MovieCollection, MovieGenre


logger = logging.getLogger(__name__)


class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format="json"):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json["token"] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def request_count(request):
    data = {"request_count": cache.get("request_count", 0)}
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def reset_request_count(request):
    cache.delete("request_count")
    data = {"message": "request count reset successfully"}
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def home_page(request):
    page = request.GET.get("page")

    try:
        client = MayaApiClient()
        data = client.get_movie_list(page=page)
    except ApiConnectionErrorException as e:
        pass

    except ApiTimeoutException as e:
        pass

    except Exception as e:
        pass
    else:
        # API seems to be return is_success flag in case of failure
        if "is_success" not in data:
            # TODO : a celery task to feed api data into db
            next_page = data.get("next")
            previous_page = data.get("previous")
            api_movie_url = client._build_url("movies/")
            if next_page:
                next_page = next_page.replace(api_movie_url, request.path)
                data["next"] = next_page
            if previous_page:
                previous_page = previous_page.replace(api_movie_url, request.path)
                data["previous"] = previous_page
            return Response(data, status=status.HTTP_200_OK)

    return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class MovieViewset(viewsets.ModelViewSet):
    """
    Viewsets for movies
    """

    serializer_class = MovieSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Movie.objects.all()


class CollectionViewset(viewsets.ModelViewSet):
    """
    Viewset for  Movie collections
    """

    serializer_class = CollectionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.collections.prefetch_related("movies")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
