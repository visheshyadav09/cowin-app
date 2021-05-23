from django.http import HttpResponse, response
from django.shortcuts import redirect, render
import requests
from datetime import date
import json
from .utils import *
# Create your views here.


def index(request):
    template = 'cowin_app/index.html'
    return render(request, template)

def get_otp(request):
    try:
        mobile = request.POST['mobile']
    except:
        return HttpResponse("Mobile number not found", status = 500)
    
    url = 'http://127.0.0.1:8001/api/'
    data = {
        'mobile': mobile
    }

    response = requests.post(url, data=data)
    print()
    request.session['txnId'] = json.loads(response.content)["txnId"]
    request.session['mobile'] = mobile
    return HttpResponse(status=200)

def verify_otp(request):
    try:
        otp = request.POST['otp']
    except:
        return HttpResponse("Mobile number not found")
    
    url = 'http://127.0.0.1:8001/api/'
    data = {
        'mobile': request.session['mobile'],
        'txnId': request.session['txnId'],
        'otp': otp,
    }
    response = requests.post(url, data=data)
    status_code = response.status_code
    if status_code == 200:
        data = json.loads(response.content)
        request.session['token'] = data['token']
    return HttpResponse(status_code)

def get_districts(request):
    try:
        state_id = request.POST['state_id']
    except:
        return HttpResponse("Please select valid state")

    url = 'http://127.0.0.1:8001/api/get-districts/' + state_id + '/'
    response = requests.get(url)
    districts = json.loads(response.content)
    return HttpResponse(json.dumps(districts))

def get_slots(request):
    try:
        district_id = request.POST['district_id']
    except:
        return HttpResponse("Please select valid district")

    appointment_date = date.today().strftime('%d-%m-%Y')
    url = 'get-slots/' + district_id + '/' + appointment_date + '/'
    response = requests.get(url)

def subscribe(request):
    template = "cowin_app/subscribe.html"
    states = get_states()
    beneficiaries = get_beneficiary(request.session['token'])
    if not beneficiaries:
        return redirect(index)
    context = {
        'states': states,
        'beneficiaries': beneficiaries['beneficiary']
    }
    return render(request, template, context)


