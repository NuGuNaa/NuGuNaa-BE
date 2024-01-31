from .models import *
from rest_framework import serializers


class PetitionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition_Detail
        fields = '__all__'
        

class PetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition
        fields = '__all__'