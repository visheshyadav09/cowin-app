from django.db import models


class Subscription(models.Model):
    email = models.EmailField(max_length= 20, null= True, blank= True)
    beneficiary_id = models.IntegerField(null=True, blank=True, unique= True)
    district_id = models.IntegerField(blank  = True, null = True)

    def _str_(self):
        return self.district_id