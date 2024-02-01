from django.db import models


class Petition(models.Model):
    BILL_NO = models.CharField(primary_key=True, max_length=30, null=False, blank=False)
    BILL_NAME = models.CharField(max_length=100, null=False, blank=True)
    PROPOSER = models.CharField(max_length=30, null=False, blank=True)
    PROPOSER_DT = models.DateField(null=False, blank=False)
    COMMITTEE_DT = models.DateField(null=False, blank=False)
    
    def __str__(self):
        return self.BILL_NAME
    
    
class Petition_Detail(models.Model):
    BILL_NO = models.OneToOneField(Petition, primary_key=True, null=False, blank=False, on_delete=models.CASCADE)
    APPROVER = models.CharField(max_length=30, null=False, blank=False)
    CURR_COMMITTEE = models.CharField(max_length=30, null=False, blank=False)
    LINK_URL = models.CharField(max_length=255, null=False, blank=False)
    
    def __str__(self):
        return self.BILL_NO
    
    
class Petition_File(models.Model):
    BILL_NO = models.OneToOneField(Petition, primary_key=True, null=False, blank=False, on_delete=models.CASCADE)
    petition_file_url = models.CharField(max_length=100, null=True, blank=False)
    content = models.TextField(null=True)
    
    def __str__(self):
        return self.content