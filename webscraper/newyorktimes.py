import requests as r
import json
import sys
sys.path.append(
    "/Users/felixbieswanger/Desktop/Uni_Stuff/Bachelorarbeit/OpionionMining")
import keys

key = keys.get_key("newyorktimes")


response = r.get(
    "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=digitization&sort=newest&page=1&api-key="+key).content

result = json.loads(response)["response"]

for doc in result["docs"]:
    print(doc["headline"], doc["pub_date"])
    print()

