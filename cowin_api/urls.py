from django.urls import path
from .views import *

urlpatterns = [
    path('', GetToken.as_view(), name="get-token"),
]