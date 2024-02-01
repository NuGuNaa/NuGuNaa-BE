from .models import *
from rest_framework import serializers


class DebateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debate
        fields = '__all__'