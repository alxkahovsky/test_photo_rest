from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import PhotosListView


router = DefaultRouter()
router.register(r'api', PhotosListView, basename='photo')
urlpatterns = router.urls
