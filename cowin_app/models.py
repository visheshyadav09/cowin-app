from django.db import models

# Create your models here.

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

class Pincode(models.Model):
    city_name = models.CharField(max_length=200)
    pincode = models.IntegerField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.city_name + ' ' + self.district.district_name