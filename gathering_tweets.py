
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from math import cos, pi
from geopy.geocoders import Nominatim


#Variables that contains the user credentials to access Twitter API
consumer_key = 'oeaiWzPmHLx20OLsp5g5QPFbw'
consumer_secret = '3b55vyoax4DIkhvTX6KUGP9sSjhxo9ZxOfpUUtsz6tpPVfZfw3'
access_token = '926830219356340225-z2qjfLCagnxp99AL4UhzQ94LUQbo9RR'
access_secret = 'uX5IWIi0ERKLySSQEYIVOSIcjEuHCmJlPwEK2zSLLLgGk'

#This is a basic listener that just prints received tweets to stdout.

tweet_data = list()
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)
    stream.filter(track = ['UMD'])
    stream.filter(count = [1])

import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data = []
tweets_file = open("tweets.txt", "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

print ("tweets here", len(tweets_data))

tweets = pd.DataFrame()

tweets['id'] = map(lambda tweet: tweet.get('id', None),tweets_data)
tweets['text'] = map(lambda tweet: tweet.get('text', None),tweets_data)

print(tweets.head())
print(tweets)
