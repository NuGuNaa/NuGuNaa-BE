from django.db import models
from petitions.models import *


class Debate(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    member_announcement_date = models.DateField(null=False, blank=False)
    debate_date = models.DateTimeField(null=False, blank=False)
    estimated_time = models.CharField(max_length=10, null=False, blank=False, default="1시간")
    petition_id = models.OneToOneField(Petition, null=False, blank=False, on_delete=models.CASCADE)
    debate_code_O = models.CharField(max_length=30, null=False, blank=False)
    debate_code_X = models.CharField(max_length=30, null=False, blank=False)
    
    
