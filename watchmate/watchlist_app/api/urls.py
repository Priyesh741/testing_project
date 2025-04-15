from watchlist_app.api import views
from django.urls import path

urlpatterns = [
    path('list/',views.WatchListAV.as_view(),name="movie_list"),
    path('<int:pk>/',views.WatchDetailAV.as_view(),name="movie_details"),
    path('platform/',views.StreamPlatformAV.as_view(),name="platform_list"),
    path('platform/<int:pk>/',views.StreamDetailAV.as_view(),name="platform_list"),
]
