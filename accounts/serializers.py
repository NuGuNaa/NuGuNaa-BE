from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        user = User.objects.create_user(
            user_name = validated_data['user_name'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user