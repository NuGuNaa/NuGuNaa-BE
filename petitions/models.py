from django.db import models


class Petition_Detail(models.Model):
    BILL_NO = models.CharField(primary_key=True, max_length=30, null=False, blank=False)
    APPROVER = models.CharField(max_length=30, null=False, blank=False)
    CURR_COMMITTEE = models.CharField(max_length=30, null=False, blank=False)
    LINK_URL = models.CharField(max_length=255, null=False, blank=False)
    petition_file = models.FileField(upload_to="")
    
    def __str__(self):
        return self.BILL_NO
    
    
class Petition(models.Model):
    BILL_NO = models.OneToOneField(Petition_Detail, primary_key=True, max_length=30, null=False, blank=False, on_delete=models.CASCADE)
    BILL_NAME = models.CharField(max_length=100, null=False, blank=True)
    PROPOSER = models.CharField(max_length=30, null=False, blank=True)
    PROPOSER_DT = models.DateField(null=False, blank=False)
    COMMITTEE_DT = models.DateField(null=False, blank=False)
    content = models.TextField(null=False)
    
    def __str__(self):
        return self.BILL_NAME