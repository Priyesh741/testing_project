from rest_framework import serializers
from watchlist_app.models import *
from rest_framework import validators

# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name too short")
#     else:
#         return value
    

class MovieSerializer(serializers.ModelSerializer):
    #custom serializer
    len_name=serializers.SerializerMethodField()
    class Meta:
        model=Movie

        fields="__all__"
        # your to specific field 
        # fields=['name','description','id']
        # you want to exclude some fields
        # exclude=['active']

    def get_len_name(self,object):
        return len(object.name)


        #object level validators
    def validate(self, data):
        if data['name']==data['description']:
            raise serializers.ValidationError("Name should not be same as description")
        else:
            return data
    

    # field level validators
    def validate_name(self,value):
        if len(value)<2:
            raise serializers.ValidationError("Name too short")
        else:
            return value

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