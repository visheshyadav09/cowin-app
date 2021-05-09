from django.urls import path
from .views import *

urlpatterns = [
    path('generatetoken/', Generate.as_view(), name="token"),
]