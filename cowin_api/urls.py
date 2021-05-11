from django.urls import path
from .views import *

urlpatterns = [
    path('getbeneficiary/', GetBeneficiaries.as_view(), name="token"),
]