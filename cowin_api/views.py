from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from django.http import HttpResponse
from django.views import View
from cowin_api import cowin_secret
import requests
import json
import hashlib
from datetime import datetime, timedelta
# Create your views here.

OTP_URL             = cowin_secret.OTP_URL
CONFIRM_OTP         = cowin_secret.CONFIRM_OTP
GET_STATES          = cowin_secret.GET_STATES
GET_DISTRICTS       = cowin_secret.GET_DISTRICTS
SECRET              = cowin_secret.SECRET
headers             = cowin_secret.headers




class GetToken(APIView):

    def send_otp(self, mobile):

        data = {
            "mobile": mobile,
            "secret": SECRET
        }
        response = json.loads(requests.post(OTP_URL, data=json.dumps(data), headers=headers).content)
        txnId = response['txnId']
        return txnId

    def generate_token(self, otp, txnId):
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()
        data = {
            "otp": otp_hash,
            "txnId": txnId
        }
        response = requests.post(CONFIRM_OTP, data=json.dumps(data), headers=headers).content
        if response == b'Unauthenticated access!':
            return False
        response = json.loads(response)
        self.token = response['token']
        return True

    def post(self, request):
        token = None
        try:
            mobile = request.POST['mobile']
            otp = request.POST.get('otp')
            txnId = request.POST.get('txnId')
        except:
            return HttpResponse(json.dumps({'status': 'failure', 'message': 'Mobile number missing'}))
        try:
            user = Users.objects.get(mobile_number=mobile)
            token = user.user_token
            token_expire = user.token_expire
            if token_expire:
                if token_expire.replace(tzinfo=None) < datetime.now():
                    token = None
        except:
            user = Users.objects.create(mobile_number=mobile)

        if not token:
            if not otp:
                txnId = self.send_otp(mobile)
                return HttpResponse(json.dumps({'status': 'success', 'message': 'OTP sent successfully', 'txnId': txnId}))
            else:
                generate_token = self.generate_token(otp, txnId)
                if not generate_token:
                    return HttpResponse(json.dumps({'status': 'failure', 'message': 'Incorrect OTP'}))
                user.user_token = self.token
                user.token_expire = datetime.now() + timedelta(days=1)
                user.save()
                return HttpResponse(json.dumps({'status': 'success', 'token': self.token}))

        return HttpResponse(json.dumps({'status': 'success', 'token': token}))


                
