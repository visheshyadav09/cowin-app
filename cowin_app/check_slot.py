from .models import *

district_ids = Subscription.objects.order_by().values('district_id').distinct()

for district in district_ids:
    id = district['district_id']
    #check for slots
    #if slot available for id:
        #emails = Subscription.objects.filter(district_id = id)
        #for email in emails:
            #send_email(email)