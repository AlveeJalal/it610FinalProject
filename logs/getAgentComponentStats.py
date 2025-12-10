#!/usr/bin/env python3

import json
from base64 import b64encode

from dotenv import load_dotenv
import os

import requests  
import urllib3

load_dotenv()

#Configuration
endpoint = '/agents/002/stats/agent'

protocol = 'https'
host = '172.23.128.164'
port = '55000'
user = os.environ.get('API_USERNAME')
password = os.environ.get('API_PASSWORD')

#Disable insecure https warnings (for self-signed SSL certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_response(request_method, url, headers, verify=False, body=None):
    """Get API result"""
    if body is None:
        body = {}

    request_result = getattr(requests, request_method.lower())(url, headers=headers, verify=verify, data=body)

    if request_result.status_code == 200:
        return json.loads(request_result.content.decode())
    else:
        raise Exception(f"Error obtaining response: {request_result.json()}")


base_url = f"{protocol}://{host}:{port}"
login_url = f"{base_url}/security/user/authenticate"
basic_auth = f"{user}:{password}".encode()
headers = {
           'Authorization': f'Basic {b64encode(basic_auth).decode()}',
           'Content-Type': 'application/json'
           }
headers['Authorization'] = f'Bearer {get_response("POST", login_url, headers)["data"]["token"]}'

#Request
response = get_response("GET", url=base_url + endpoint, headers=headers)

print(json.dumps(response, indent=4, sort_keys=True))
with open("lastKeepAlive.log", "a") as f:
    f.write(json.dumps(response, indent=4, sort_keys=True))
