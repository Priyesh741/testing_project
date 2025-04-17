from rest_framework import serializers
from watchlist_app.models import *
from rest_framework import validators

# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name too short")
#     else:
#         return value

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        # fields='__all__'
        exclude=['watchlist']

class WatchListSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(many=True,read_only=True)

    #custom serializer
    len_name=serializers.SerializerMethodField()
    class Meta:
        model=WatchList

        fields="__all__"
        # your to specific field 
        # fields=['name','description','id']
        # you want to exclude some fields
        # exclude=['active']

    def get_len_name(self,object):
        return len(object.title)

class StreamPlatformSerializer(serializers.ModelSerializer):
    #nested serializers
    watchlist=WatchListSerializer(many=True,read_only=True)
    #watchlist=serializers.StringRelatedField(many=True,read_only=True)  #it return only movie name using in model def __str__()
    #watchlist=serializers.PrimaryKeyRelatedField(many=True,read_only=True) #it return id of movie 
    
    #watchlist=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="movie_details") #view name is url name

    class Meta:
        model=StreamPlatform
        fields="__all__"


    #object level validators
    # def validate(self, data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError("Name should not be same as description")
    #     else:
    #         return data
    

    # # field level validators
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name too short")
    #     else:
    #         return value

# class MovieSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(validators=[name_length])
#     description=serializers.CharField()
#     active=serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name=validated_data.get('name',instance.name)
#         instance.description=validated_data.get('description',instance.description)
#         instance.active=validated_data.get('active',instance.active)
#         instance.save()
#         return instance
    
#     #object level validators
#     def validate(self, data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("Name should not be same as description")
#         else:
#             return data
    

    #field level validators
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name too short")
    #     else:
    #         return value