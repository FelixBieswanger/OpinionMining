import sys
sys.path.append(
    "/Users/felixbieswanger/Desktop/Uni_Stuff/Bachelorarbeit/OpionionMining")
import requests as r
import keys
import useragent 
import json

key = keys.get_key("zeit")["key"]
headers = {
    "X-Auth-Token":key
}

result = json.loads(r.get("http://api.zeit.de/content/", headers=headers).content)
print(result)
