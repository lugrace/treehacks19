
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
from math import cos, pi
from geopy.geocoders import Nominatim


#Variables that contains the user credentials to access Twitter API
consumer_key = 'oeaiWzPmHLx20OLsp5g5QPFbw'
consumer_secret = '3b55vyoax4DIkhvTX6KUGP9sSjhxo9ZxOfpUUtsz6tpPVfZfw3'
access_token = '926830219356340225-z2qjfLCagnxp99AL4UhzQ94LUQbo9RR'
access_secret = 'uX5IWIi0ERKLySSQEYIVOSIcjEuHCmJlPwEK2zSLLLgGk'

tweet_data = []

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
for tweet in tweepy.Cursor(api.search,
                           q="UMD",
                           count=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items(2500):     # the values inside items defines how many searches we want
    print(tweet.text)
    tweet_data.append(tweet.text)
