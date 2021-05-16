from django.db import models
# Create your models here.
class Users(models.Model):
    mobile_number = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        mobile = str(self.mobile_number)
        date = self.token_expire.strftime("%m/%d/%Y, %H:%M:%S") if self.token_expire else 'None'
        return mobile + '-->' + date
    
class State(models.Model):
    state_name = models.CharField(max_length=200)
    state_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.state_name

class District(models.Model):
    district_name = models.CharField(max_length=200)
    district_id = models.IntegerField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.district_name + ' ' + self.state.state_name

class Subscription(models.Model):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, blank = True, null = True)
    email = models.CharField(max_length= 20, null= True, blank= True)
    beneficiary_id = models.IntegerField(null=True, blank=True, unique= True)
    district_id = models.ForeignKey(District, on_delete=models.SET_NULL, blank  = True, null = True)
    appointment_confirmation_no = models.CharField(max_length=50, blank = True, null = True)


    def __str__(self):
        return self.beneficiary_id


class Pincode(models.Model):
    city_name = models.CharField(max_length=200)
    pincode = models.IntegerField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.city_name + ' ' + self.district.district_name

    

