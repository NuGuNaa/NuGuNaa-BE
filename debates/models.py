from django.db import models
from petitions.models import *
from accounts.models import *


class Debate(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    member_announcement_date = models.DateTimeField(null=False, blank=False)
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
    raffle_check = models.BooleanField(null=True, blank=False) # 추첨됐는지 확인
    
    
class Debate_Statement(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    debate_id = models.ForeignKey(Debate, null=False, blank=False, on_delete=models.CASCADE)
    statement_type = models.CharField(max_length=20, null=False, blank=False)
    content = models.TextField()
    is_chatgpt = models.BooleanField(default=False, null=False, blank=False)
    position = models.IntegerField(null=True, blank=False) # 찬성: 0, 반대: 1
    
    
class Statement_User(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    statement_id = models.ForeignKey(Debate_Statement, null=False, blank=False, on_delete=models.CASCADE)
    user_email = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)