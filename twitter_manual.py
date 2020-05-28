import json
import keys
import oauth2 

keys = keys.get_key("twitter")

consumer = oauth2.Consumer(key=keys["api-key"], secret=keys["api-key-secret"])
token = oauth2.Token(key=keys["accsess-token"], secret=keys["accsess-token-secret"])
client = oauth2.Client(consumer,token)


settings = {
    "q":"Digitale Transformation",
    "count":"100",
    "result_type":"recent",
    "tweet_mode":"popular",
    "lang":"de"
}

parameter_string = ""
for key, value in zip(settings.keys(), settings.values()):
    parameter_string += key
    parameter_string += "="
    parameter_string += value
    parameter_string += "&"

parameter_string = parameter_string[:-2] + ".json"

timeline_endpoint = "https://api.twitter.com/1.1/tweets/fullarchive/hdm"+parameter_string
response, data = client.request(timeline_endpoint)

data = json.loads(data)
tweets = data["statuses"]

for tweet in tweets:
    print(tweet["created_at"])


    



