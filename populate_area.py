from cowin import settings
from cowin import wsgi
from cowin_api.models import State, District, Pincode
import requests
import json
import hashlib
from cowin_api import cowin_secret

class Populate():
    OTP_URL             = cowin_secret.OTP_URL
    CONFIRM_OTP         = cowin_secret.CONFIRM_OTP
    GET_STATES          = cowin_secret.GET_STATES
    GET_DISTRICTS       = cowin_secret.GET_DISTRICTS
    SECRET              = cowin_secret.SECRET
    headers             = cowin_secret.headers
    area                = {}

    def __init__(self, mobile):
        self.send_otp(mobile)
        print("Done")

    def send_otp(self, mobile):

        data = {
            "mobile": mobile,
            "secret": self.SECRET
        }
        response = json.loads(requests.post(self.OTP_URL, data=json.dumps(data), headers=self.headers).content)
        txnId = response['txnId']
        self.generate_token(txnId)
        return

    def generate_token(self, txnId):
        otp = input("Enter OTP: ")
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()
        data = {
            "otp": otp_hash,
            "txnId": txnId
        }
        response = json.loads(requests.post(self.CONFIRM_OTP, data=json.dumps(data), headers=self.headers).content)
        token = response['token']
        self.headers["Authorization"] = f'Bearer {token}'
        print(token)
        self.get_states()
        return

    def get_states(self):
        response = json.loads(requests.get(self.GET_STATES, headers=self.headers).content)
        states = response['states']
        for state in states:
            self.get_districts(state)
        return

    def get_districts(self, state):
        response = json.loads(requests.get(self.GET_DISTRICTS + str(state['state_id']), headers=self.headers).content)
        districts = response['districts']
        self.save_data(state, districts)
        return

    def save_data(self, state, districts):
        self.area[state['state_id']] = {
            "name": state['state_name'],
            "districts": districts
        }
        if str(state['state_id']) == "36":
            with open("data.txt", "w+") as f:
                f.write(str(self.area))

        return



mobile = "9370667988"
# Populate(mobile=mobile)
Populate().get_states()

