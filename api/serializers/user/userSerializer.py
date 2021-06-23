from rest_framework import serializers
from api.models import User

class UserSignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','phone_number','dob','gender','profile_image','role')


