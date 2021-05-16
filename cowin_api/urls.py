from django.urls import path
from .views import *



urlpatterns = [
    path('', GetToken.as_view(), name="get-token"),
    path('get-beneficiary/', GetBeneficiaries.as_view(), name="get-beneficiary"),
    path('get-calender-by-district/<district_id>/<date>/',GetCalenderbydistrict.as_view(),name='get-calender-by-district'),
    path('get-states/', GetState.as_view(), name="get-states"),
    path('get-districts/<state_id>/', GetDistrict.as_view(), name="get-districts"),
    path('schedule-appointment/<beneficiary_id>/', ScheduleAppointment.as_view(), name="schedule-appointment"),
]