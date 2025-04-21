from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','password2']

        extra_kwargs={'password':{'write_only':True

        }}

    def save(self):
        #validate_data ->This is a dictionary containing all the data that has been validated by the serializer.
        #It only becomes available after you call is_valid() on the serializer.
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password!=password2:
            raise serializers.ValidationError({'error':"password and confirm password are not same"})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'email is already exist'})
        
        account=User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account
