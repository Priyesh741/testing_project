from watchlist_app.api import views
from django.urls import path

urlpatterns = [
    path('list/',views.MovieListAV.as_view(),name="movie_list"),
    path('<int:pk>/',views.MovieDetailAV.as_view(),name="movie_details")
]
