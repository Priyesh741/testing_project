from watchlist_app import views
from django.urls import path

urlpatterns = [
    path('list/',views.movielist_view,name="movie_list"),
    path('<int:pk>/',views.movie_detail,name="movie_details")
]
