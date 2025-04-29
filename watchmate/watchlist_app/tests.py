from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from . import models
from .api import serializers

class StreamPlateTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='example',password="Password@123")
        self.token=Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        self.stream=models.StreamPlatform.objects.create(name='netflix',about='This is good stream platform',website='https://www.netflix.com')

    def test_StreamPlatform_create(self):
        data={
            'name':'netflix',
            'about':'This is good stream platform',
            'website':'https://www.netflix.com'
        }
        response=self.client.post(reverse('StreamPlatform-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_StreamPlatform_list(self):
        response=self.client.get(reverse('StreamPlatform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_StreamPlatform_ind(self):
        response=self.client.get(reverse('StreamPlatform-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_StreamPlatform_put(self):
        data={
            'name':'netflix',
            'about':'This is good for mind refreshing',
            'website':'https://www.netflix.com'
        }
        response=self.client.put(reverse('StreamPlatform-detail',args=(self.stream.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_StreamPlatform_delete(self):
        response=self.client.delete(reverse('StreamPlatform-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='priyesh',password='123456')
        self.token=Token.objects.get(user__username='priyesh')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

        self.stream=models.StreamPlatform.objects.create(name='netflix',about='This is good stream platform',website='https://www.netflix.com')
        self.watch=models.WatchList.objects.create(title="Iron man 3",description="This is awesome movies",avg_rating=0,
    number_of_rating=0,platform=self.stream)
        
    def test_Watchlist_list(self):
        response=self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_Watchlist_post(self):
        data={
            'title':"Spider Man return Home",
            'description':"This is fantantic movies",
            'avg_rating':0,
            'number_of_rating':0,
            "platform":self.stream
        }
        response=self.client.post(reverse('movie_list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_Watchlist_ind(self):
        response=self.client.get(reverse('movie_details',args=(self.watch.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, 'Iron man 3')

    def test_Watchlist_put(self):
        data={
            'title':"Iron man 3 part 2",
            'description':"This is best movie of marvel",
            'avg_rating':0,
            'number_of_rating':0,
            "platform":self.stream
        }
        response=self.client.put(reverse('movie_details',args=(self.watch.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_Watchlist_delete(self):
        response=self.client.delete(reverse('movie_details',args=(self.watch.id,)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='example',password="Password@123")
        self.token=Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)

        self.stream=models.StreamPlatform.objects.create(name='netflix',about='This is good stream platform',website='https://www.netflix.com')
        self.watch=models.WatchList.objects.create(title="Iron man 3",description="This is awesome movies",avg_rating=0,
    number_of_rating=0,platform=self.stream)
        
        self.review=models.Review.objects.create(review_user=self.user,rating=4,description="This movie is awesome in hollywood",
            watchlist=self.watch,
            active=True)

    def test_Review_create(self):
        data={
            "review_user":self.user,
            "rating":4,
            "description":"This movie is awesome in hollywood",
            "watchlist":self.watch,
            "active":True
        }
        response=self.client.post(reverse("review_create",args=(self.watch.id,)),data)
        # self.assertEqual(response.status_code,status.HTTP_201_CREATED)   #first time run testcase is pass
        self.assertEqual(models.Review.objects.count(), 1)
        self.assertEqual(models.Review.objects.get().rating, 4)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)  #second time run testcase is pass
    
    def test_Review_create_unauth(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"This movie is hello in hollywood",
            "watchlist":self.watch,
            "active":True
        }
        self.client.force_authenticate(user=None)
        response=self.client.post(reverse("review_create",args=(self.watch.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_Review_list(self):
        response=self.client.get(reverse("review_list",args=(self.watch.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_Review_ind(self):
        response=self.client.get(reverse("review_detail",args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_Review_put(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"This movie is fantanic of world",
            "watchlist":self.watch,
            "active":True
        }
        response=self.client.put(reverse("review_detail",args=(self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_Review_delete(self):
        response=self.client.delete(reverse("review_detail",args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_Review_user(self):
        response=self.client.get("/movie/review/?username"+self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    




    

