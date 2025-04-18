from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from watchlist_app.models import *
# from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from .serializers import *
from .permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from rest_framework import status
from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly


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
    permission_classes=[ReviewUserOrReadOnly]
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer): 
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)

        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist,review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed the movie")
        
        if watchlist.number_of_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating+serializer.validated_data['rating']/2)
        
        watchlist.number_of_rating=watchlist.number_of_rating+1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)

class ReviewList(generics.ListCreateAPIView):
    #queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
#self.kwargs is a dictionary of keyword arguments captured from the URL pattern (like path('movie/<int:pk>/reviews/', ...)).
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[ReviewUserOrReadOnly]
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
    
class StreamplatformVS(viewsets.ModelViewSet):
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer
    
###############################################################################################
###################################################using viewsets   
# class StreamplatformVS(viewsets.ViewSet):
#     def list(self,request):
#         queryset=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     def retrieve(self,request,pk=None):
#         queryset=StreamPlatform.objects.all()
#         watchlist=get_object_or_404(queryset,pk=pk)
#         serializer=StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
############################################################################################
###########################################################################################

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
        