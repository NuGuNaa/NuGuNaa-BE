from .models import *
from rest_framework import serializers


class PetitionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition_File
        fields = '__all__'
        

class PetitionSerializer(serializers.ModelSerializer):
    petition_file = PetitionFileSerializer(read_only=True)
    
    class Meta:
        model = Petition
        fields = ['BILL_NO', 'BILL_NAME', 'PROPOSER', 'PROPOSER_DT', 'COMMITTEE_DT', 'petition_file']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'petition_file' in representation and representation['petition_file'] is not None:
            content = representation['petition_file'].get('content')
            representation['petition_file'] = {'content': content}
        return representation
        
        
class PetitionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition_Detail
        fields = '__all__'