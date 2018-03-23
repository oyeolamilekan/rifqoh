from django.db import models
from django.conf import settings

# Create your models here.

class Shop(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True,on_delete=True)
	shop_name = models.CharField(max_length=300,unique=True)

