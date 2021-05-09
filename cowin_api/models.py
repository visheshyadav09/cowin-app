from django.db import models
# Create your models here.
class Users(models.Model):
    mobile_number = models.IntegerField(null=True, blank=True)
    user_token = models.CharField(max_length=200, blank=True)
    token_expire = models.DateTimeField(null=True,blank=True)



    

