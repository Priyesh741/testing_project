from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from watchlist_app.models import *
# from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework import generics,mixins



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
#####################function api view
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

class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer

    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        movie=WatchList.objects.get(pk=pk)
        serializer.save(watchlist=movie)

class ReviewList(generics.ListCreateAPIView):
    #queryset=Review.objects.all()
    serializer_class=ReviewSerializer

#self.kwargs is a dictionary of keyword arguments captured from the URL pattern (like path('movie/<int:pk>/reviews/', ...)).
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer

###########################################################################################
###############################Generic view using mixins
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer

#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

############################################################################################
###################################### using APIView
# class ReviewAV(APIView):
#     def get(self,request):
#         review=Review.objects.all()
#         serializer=ReviewSerializer(review,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer=ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
        
# class ReviewDetailAV(APIView):
#     def get(self,request,pk):
#         try:
#             review=Review.objects.get(pk=pk)
#         except Review.DoesNotExist:
#             return Response({'error':'Invalid Input'},status=status.HTTP_400_BAD_REQUEST)

#         serializer=ReviewSerializer(review)
#         return Response(serializer.data)
#     def put(self,request,pk):
#         try:
#             review=Review.objects.get(pk=pk)
#         except Review.DoesNotExist:
#             return Response({'error':'Invalid Input'},status=status.HTTP_400_BAD_REQUEST)
#         serializer=ReviewSerializer(review,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
###########################################################################################

class WatchListAV(APIView):
    def get(self,request):
        movie=WatchList.objects.all()
        serializer=WatchListSerializer(movie,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Created": "successful"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class WatchDetailAV(APIView):
    def get(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"errors":"Movie not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"errors":"Movie not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response({"delete":"Content deleted"},status=status.HTTP_204_NO_CONTENT)
    

class StreamPlatformAV(APIView):
    def get(self,request):
        platform=StreamPlatform.objects.all()
        serilaizer=StreamPlatformSerializer(platform,many=True)
        return Response(serilaizer.data)
    
    def post(self,request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Created sucessfully'},status=status.HTTP_201_CREATED)

        else:
            return Response({"error":"Invalid fields"},serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
class StreamDetailAV(APIView):
    def get(self,request,pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"errors":"Movie not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"errors":"Movie not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Updated Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'Invalid Input'},serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response({'message':"Deleted SuccessFully"},status=status.HTTP_204_NO_CONTENT)
        