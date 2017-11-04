
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import queue
from tweepy import Stream
import tweepy
from math import cos, pi
from geopy.geocoders import Nominatim


# TWITTER API CREDENTIALS
consumer_key = 'oeaiWzPmHLx20OLsp5g5QPFbw'
consumer_secret = '3b55vyoax4DIkhvTX6KUGP9sSjhxo9ZxOfpUUtsz6tpPVfZfw3'
access_token = '926830219356340225-z2qjfLCagnxp99AL4UhzQ94LUQbo9RR'
access_secret = 'uX5IWIi0ERKLySSQEYIVOSIcjEuHCmJlPwEK2zSLLLgGk'

# acronym dictionary

f = open("college_acronyms.txt", 'r')
colleges = {}
line = f.readline()
while line != "":
    line = line.split(' - ')
    fullname = line[1].split(', ')[:-1]
    for x in fullname:
        colleges[x] = line[0]
    line = f.readline()

input_word = 'University of Maryland'
acronym_word = colleges[input_word]
tweet_data = queue.Queue()

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, q=input_word, count=100, result_type="recent", include_entities=True, lang="en").items(1):     # the values inside items defines how many searches we want
    #print(tweet.text)
    tweet_data.put(tweet.text)
for tweet in tweepy.Cursor(api.search, q=acronym_word, count=100, result_type="recent", include_entities=True, lang="en").items(1):     # the values inside items defines how many searches we want
    #print(tweet.text)
    tweet_data.put(tweet.text)

print(colleges)
