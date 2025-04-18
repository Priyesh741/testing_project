from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class StreamPlatform(models.Model):
    name=models.CharField(max_length=50)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=100)

    def __str__(self):
        return self.name

class WatchList(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    avg_rating=models.FloatField(default=0)
    number_of_rating=models.IntegerField(default=0)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name='watchlist')
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="review_user")
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description=models.CharField(max_length=200)
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='reviews')
    active=models.BooleanField(default=True)
    create=models.DateTimeField(auto_now_add=True)   #When it's set: Only once, when the object is created.
    update=models.DateTimeField(auto_now=True)   #When it's set: Every time the object is saved (created or updated).

    def __str__(self):
        return self.watchlist.title +" *Reviews "+ str(self.rating)
