from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from watchlist_app.models import *
# from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from .serializers import *
from rest_framework import status


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

#####################################################################################
##################################################################################  the code is replace by ApiView
# @api_view(['GET','POST'])
# def movielist_view(request):
#     if request.method=='GET':
#         movie=Movie.objects.all()
#         serializer=MovieSerializer(movie,many=True)
#         return Response(serializer.data)
    
#     if request.method=='POST':
#         serializer=MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors)

# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request,pk):
#     if request.method=='GET':
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"error":"Movie not found"},status=status.HTTP_404_NOT_FOUND)
#         serializer=MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method=='PUT':
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method=='DELETE':
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
###########################################################################################

class MovieListAV(APIView):
    def get(self,request):
        movie=Movie.objects.all()
        serializer=MovieSerializer(movie,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Created": "successful"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class MovieDetailAV(APIView):
    def get(self,request,pk):
        try:
            movie=Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"errors":"Movie not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer=MovieSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            movie=Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"errors":"Movie not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer=MovieSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        movie=Movie.objects.get(pk=pk)
        movie.delete()
        return Response({"delete":"Content deleted"},status=status.HTTP_204_NO_CONTENT)
        
    
        