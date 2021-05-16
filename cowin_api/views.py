from cowin_api import serializers
from cowin_api.serializers import StateSerializers, DistrictSerializers
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from django.http import HttpResponse
from django.views import View
from cowin_api import cowin_secret
import requests
import json
import hashlib
from datetime import datetime, timedelta
from django.http import HttpResponseNotFound
from rest_framework.permissions import IsAuthenticated   
# Create your views here.

OTP_URL                     = cowin_secret.OTP_URL
CONFIRM_OTP                 = cowin_secret.CONFIRM_OTP
GET_STATES                  = cowin_secret.GET_STATES
GET_DISTRICTS               = cowin_secret.GET_DISTRICTS
GET_BENEFICIARY             = cowin_secret.GET_BENEFICIARY
GET_CALENDAR_BY_DISTRICT    = cowin_secret.GET_CALENDAR_BY_DISTRICT
SCHEDULE_APPOINTMENT        = cowin_secret.SHCEDULE_APPOINTMENT
SECRET                      = cowin_secret.SECRET
headers                     = cowin_secret.headers


def handler404(request,exception):
    return HttpResponseNotFound("Daa wassa WOOOPSY!")



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
        
        user = Users.objects.get_or_create(mobile_number=mobile)

        if not otp:
            txnId = self.send_otp(mobile)
            return HttpResponse(json.dumps({'status': 'success', 'message': 'OTP sent successfully', 'txnId': txnId}))
        else:
            generate_token = self.generate_token(otp, txnId)
            if not generate_token:
                return HttpResponse(json.dumps({'status': 'failure', 'message': 'Incorrect OTP'}), status = 422)
            request.session['token'] = self.token
            return HttpResponse(json.dumps({'status': 'success', 'message': 'token successfully created'}), status = 200)




class GetBeneficiaries(APIView):

    def post(self, request):
        try:
            token = request.session['token']
            headers["Authorization"] = f"Bearer {token}"
        except:
            return HttpResponse(json.dumps({'status':'failure','message':'Token Not Found'}))
        response = requests.get(GET_BENEFICIARY, headers=headers).content

        if response == b'Unauthenticated access!':
            return HttpResponse(json.dumps({'status':'failure','message':'Uauthenticated Access'}))

        response = json.loads(response['beneficiaries'])
    
        return HttpResponse(json.dumps({'status' : 'success', 'beneficiary' : response}))


class GetCalenderbydistrict(APIView):

    def get(self, request, district_id, date ):
        try:
            if date != datetime.strptime(date, "%d-%m-%Y").strftime('%d-%m-%Y'):
                raise ValueError
            District.objects.get(district_id=district_id)
        except Exception as e:

            if 'District matching query does not exist.' in e.args:
                return HttpResponse(json.dumps({'status':'failure','message':'District Id is Incorrect'}))
            else:
                return HttpResponse(json.dumps({'status':'failure','message':'Date format is not Correct'}))

        data={'district_id':district_id,'date':date}
        response = requests.get(GET_CALENDAR_BY_DISTRICT,params=data, headers=headers).content

        if response == b'Unauthenticated access!':
            return HttpResponse(json.dumps({'status':'failure','message':'Unauthenticated Access'}))

        response = json.loads(response)
        return HttpResponse(json.dumps({'status' : 'success', 'data' : response}), status = 200)

class GetState(APIView):
    def get(self, request):
        state = State.objects.all()
        serializer = StateSerializers(state, many = True)
        return Response(serializer.data)



class GetDistrict(APIView):
    def get(self,request,state_id):
        state = get_object_or_404(State, state_id = state_id)
        district = District.objects.filter(state = state)
        serializer = DistrictSerializers(district, many = True)
        return Response(serializer.data)

class ScheduleAppointment(APIView):
    def post(self,request,beneficiary_id):
        try:
            received_json_data = json.loads(request.body.decode("utf-8"))
            dose = received_json_data['dose']
            session_id = received_json_data['session_id']
            slot = received_json_data['slot']
        except:
            return HttpResponse(json.dumps({'status':'failure','message':'Invalid Information Given'}), status = 400)

        token = request.session['token']
        headers["Authorization"] = f"Bearer {token}"
        data = {'dose':dose , 'session_id' : session_id , 'slot' : slot , 'beneficiaries' : [beneficiary_id]}

        response = requests.post(SCHEDULE_APPOINTMENT,data = json.dumps(data), headers=headers).content
        
        if response == b'Unauthenticated access!':
            return HttpResponse(json.dumps({'status':'failure','message':'Unauthenticated Access'}), status = 401)
        
        response = json.loads(response)
        if Subscription.objects.filter(beneficiary_id = beneficiary_id).exists():
            Subscription.objects.filter(beneficiary_id = beneficiary_id).update(appointment_confirmation_no = response['appointment_confirmation_no'])

        
        return HttpResponse(json.dumps({'status' : 'success', 'data' : response}), status = 200)
    



            

        






                
