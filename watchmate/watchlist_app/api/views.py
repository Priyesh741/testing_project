from django.shortcuts import render
from rest_framework.decorators import api_view
from watchlist_app.models import *
# from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from .serializers import *
# Create your views here.
#@api_view(['GET'])
# def movielist_view(request):
#     movies=Movie.objects.all()
#     data={
#     "movies":list(movies.values())
#     }  
#     return JsonResponse(data)

# def movie_detail(request,pk):
#     movie=Movie.objects.get(pk=pk)
#     data={
#         "name":movie.name,
#         "description":movie.description,
#         "active":movie.active
#     }
#     return JsonResponse(data)

@api_view(['GET','POST'])
def movielist_view(request):
    if request.method=='GET':
        movie=Movie.objects.all()
        serializer=MovieSerializer(movie,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        serializer=MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

@api_view()
def movie_detail(request,pk):
    movie=Movie.objects.get(pk=pk)
    serializer=MovieSerializer(movie)
    return Response(serializer.data)