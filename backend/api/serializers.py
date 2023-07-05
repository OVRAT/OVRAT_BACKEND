from  rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']
class UserCreationSerilizer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username','password','email']

