from .models import *
from accounts.models import *
from rest_framework import serializers


class DebateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debate
        fields = '__all__'
        
        
class DebateApplySerializer(serializers.ModelSerializer):                   
    email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = Debate_Apply
        fields = ['petition_id', 'email', 'position']
        
    def create(self, validated_data):
        email = validated_data.pop('email')
        user = User.objects.get(email=email)
        
        debate_apply_instance = Debate_Apply.objects.create(
            email=user,
            **validated_data
        )
        return debate_apply_instance