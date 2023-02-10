import json
from  credentials import *
import requests
import tweepy


class MyStreamListener(tweepy.Stream):
 #   def __init__(self, api):
 #       self.api = api
 #       self.me = api.me()
 
    
    # get keywords
    r           = requests.get(url=API_BASE+"keyword/")
    data        = r.json()
    keywords    = [d['keyword'].lower() for d in data]

    def on_status(self, tweet):
              
        #res = any(ele in string for ele in list)
        #print(f"{tweet.user.name}:{tweet.text}:{tweet.text}")
        
        res = any(ele in tweet.text.lower() for ele in keywords)
        if res: 
            #print(f"MATCH MATCH MATCH {tweet.user.name}:{tweet.text}:{tweet.text}")
            # filter keywords
            payload =   {
                'contents': '{"text":"'+tweet.text+'"}',
                'channel': 'TWITTER',
                'contact': tweet.user.name
            }
            
            url         = API_BASE+'signal/'
            response    = requests.request("POST", url, data=payload)

    def on_error(self, status):
        print("Error detected")
        return True # Don't kill the stream
        

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

# get keywords
#r       = requests.get(url=API_BASE+"keyword/")
#data    = r.json()
#keywords    = [d['keyword'] for d in data]
    
stream 	= MyStreamListener(consumer_key,consumer_secret, access_token, access_token_secret)
#stream.filter(track=keywords, languages=["en"],locations=[-74,40,-73,41])
#stream.filter(track=keywords, languages=["en"],)
GEOBOX_TZ = [29.3399975929, -11.7209380022, 40.31659, -0.95]
stream.filter(locations=GEOBOX_TZ)
