from django.db import models

# Create your models here.
class Disease(models.Model):
        disease_id = models.CharField(max_length=50, null=False)
        disease_name = models.CharField(max_length=200, null=False)

class RiskDisease(models.Model):
        user = models.CharField(max_length=200, null=False)
        disease = models.ForeignKey(Disease)
        class Admin:
                pass
	
