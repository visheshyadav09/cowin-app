import requests
import json

def get_beneficiary(token):
    data = {
        'token': token
    }
    url = 'http://127.0.0.1:8001/api/get-beneficiary/'
    response = requests.post(url, data=json.dumps(data))
    if response.status_code == 200:
        return json.loads(response.content)
    return False

def get_states():
    url = 'http://127.0.0.1:8001/api/get-states/'
    response = requests.get(url)
    return json.loads(response.content)
