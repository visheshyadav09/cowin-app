from django.http import HttpResponse, response
from django.shortcuts import render
import requests
from datetime import date
import json
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
    print(response.status_code)
    return HttpResponse(response.status_code)

def get_beneficiary(request):
    try:
        token = request.POST['token']
    except:
        return HttpResponse("Please provide token")

    data = {
        'token': token
    }
    url = 'get-beneficiary/'
    response = requests.post(url, data=json.dumps(data))

def get_states(request):
    template = 'cowin_app/index.html'
    url = 'http://127.0.0.1:8001/api/get-states/'
    response = requests.get(url)
    context = {
        "states": json.loads(response.content)
    }
    return render(request, template, context)

def get_districts(request):
    try:
        state_id = request.POST['state_id']
    except:
        return HttpResponse("Please select valid state")

    url = 'http://127.0.0.1:8001/api/get-districts/' + state_id + '/'
    response = requests.get(url)
    return HttpResponse(status=200)

def get_slots(request):
    try:
        district_id = request.POST['district_id']
    except:
        return HttpResponse("Please select valid district")

    date = date.today().strftime('%d-%m-%Y')
    url = 'get-slots/' + district_id + '/' + date + '/'
    response = requests.get(url)

def subscribe(request):
    template = "cowin_app/subscribe.html"
    return render(request, template)


