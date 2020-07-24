import json
import tweepy
import keys

keys= keys.get_key("twitter")

auth = tweepy.OAuthHandler(keys["api-key"], keys["api-key-secret"])
auth.set_access_token(keys["accsess-token"], keys["accsess-token-secret"])
api = tweepy.API(auth,wait_on_rate_limit=True)

t = api.search(q="Digitalisierung",tweet_mode="extended",count=2,rpp=1)

for tweet in t:
    print("When:",tweet.created_at)
    print("Who:",tweet.user.screen_name)
    print("Where:",tweet.user.location)
    print(tweet.full_text)

    #print()
    #print(tweet._json)
    
