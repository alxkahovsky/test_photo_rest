from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/photos_list/', views.PhotosListView.as_view()),
    path('api/photos_list/post', views.PhotoViev.as_view()),
    path('api/photos_list/id=<int:id>/', views.PhotoViev.as_view()),
    path('api/photos_list/search_autocompliete/', views.autocompliete),
]
urlpatterns = format_suffix_patterns(urlpatterns)
