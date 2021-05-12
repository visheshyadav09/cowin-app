from django.urls import path
from .views import *

handler404 = 'cowin_api.views.handler404'


urlpatterns = [
    path('', GetToken.as_view(), name="get-token"),
    path('get-beneficiary/', GetBeneficiaries.as_view(), name="get-beneficiary"),
    path('get-calender-by-district/<district_id>/<date>/',GetCalenderbydistrict.as_view(),name='get-calender-by-district')
]