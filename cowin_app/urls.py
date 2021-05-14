from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('get-token/', get_token, name="get_token"),
]