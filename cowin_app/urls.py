from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('get-otp/', get_otp, name="get_otp"),
    path('verify-otp/', verify_otp, name="verify_otp"),
    path('get-beneficiary/', get_beneficiary, name="get_beneficiary"),
    path('get-states', get_states, name="get_states"),
    path('get-districts/', get_districts, name="get_districts"),
    path('subscribe/', subscribe, name="subscribe"),
]