import requests
import base64
import json
import keys
import oauth2 

keys = keys.get_key("twitter")

key_secret = '{}:{}'.format(keys["api-key"], keys["api-key-secret"]).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

access_token = auth_resp.json()['access_token']

print(access_token)

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

"""
"query":"from:TwitterDev lang:en",
                "fromDate":"<YYYYMMDDHHmm>", 
                "toDate":"<YYYYMMDDHHmm>",
"""


search_params = {
    'query': 'Digitalisierung lang:de',
    "fromDate": "201805120000",
    "toDate": "202005120000"
}


search_url = '{}1.1/tweets/search/fullarchive/hdm/counts.json'.format(base_url)

response = requests.get(search_url,headers=search_headers,params=search_params)
print(response.status_code)
result = json.loads(response.content)

print(result)



