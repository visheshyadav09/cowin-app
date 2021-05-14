from django.http import HttpResponse, response
from django.shortcuts import render
import requests
from datetime import date
import json
# Create your views here.


def index(request):
    template = 'cowin_app/index.html'
    context = {}
    return render(request, template, context)

def get_token(request):
    try:
        mobile = request.POST['mobile']
    except:
        return HttpResponse("Mobile number not found")
    
    url = 'api/'
    data = {
        'mobile': mobile
    }
    response = requests.post(url, json.dumps(data=data))

def get_states(request):

    url = 'get-states/'
    response = requests.get(url)

def get_districts(request):
    try:
        state_id = request.POST['state_id']
    except:
        return HttpResponse("Please select valid state")

    url = 'get_district/' + state_id + '/'
    response = requests.get(url)

def get_slots(request):
    try:
        district_id = request.POST['district_id']
    except:
        return HttpResponse("Please select valid district")

    date = date.today().strftime('%d-%m-%Y')
    url = 'get-slots/' + district_id + '/' + date + '/'
    response = requests.get(url)

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


