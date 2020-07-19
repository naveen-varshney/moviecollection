from rest_framework.routers import DefaultRouter
from .views import CollectionViewset, MovieViewset

router = DefaultRouter()
router.register(r"collections", CollectionViewset, basename="collection")
router.register(r"movies", MovieViewset, basename="movie")
urlpatterns = router.urls
