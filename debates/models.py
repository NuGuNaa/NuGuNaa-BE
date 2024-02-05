from django.db import models
from petitions.models import *
from accounts.models import *


class Debate(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    member_announcement_date = models.DateField(null=False, blank=False)
    debate_date = models.DateTimeField(null=False, blank=False)
    estimated_time = models.CharField(max_length=10, null=False, blank=False, default="1시간")
    petition_id = models.OneToOneField(Petition, null=False, blank=False, on_delete=models.CASCADE)
    debate_code_O = models.CharField(max_length=30, null=False, blank=False)
    debate_code_X = models.CharField(max_length=30, null=False, blank=False)
    
    
class Debate_Apply(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    petition_id = models.ForeignKey(Petition, null=False, blank=False, on_delete=models.CASCADE)
    email = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    position = models.IntegerField(null=True, blank=False) # 찬성: 0, 반대: 1
    
    def __str__(self):
        return self.petition_id