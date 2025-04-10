from django.shortcuts import render
#from django_restframework.decorators import api_view
from .models import *
from django.http import HttpResponse,JsonResponse

# Create your views here.
#@api_view(['GET'])
def movielist_view(request):
    movies=Movie.objects.all()
    data={
    "movies":list(movies.values())
    }
    return JsonResponse(data)

def movie_detail(request,pk):
    movie=Movie.objects.get(pk=pk)
    data={
        "name":movie.name,
        "description":movie.description,
        "active":movie.active
    }
    return JsonResponse(data)

