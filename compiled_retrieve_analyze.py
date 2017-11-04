
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import Queue
from tweepy import Stream
import tweepy
from math import cos, pi
from geopy.geocoders import Nominatim

import http.client, urllib.request, urllib.parse, urllib.error, base64
import http.client, urllib
import json

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
#---
#analyzing tweets
accessKey = 'f15920f0f61947c29e12c7f1f12174f9'
uri = 'westcentralus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'

def GetSentiment (documents):
    "Gets the sentiments for a set of documents and returns the information."

    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection (uri)
    body = json.dumps (documents)
    conn.request ("POST", path, body, headers)
    response = conn.getresponse ()
    return response.read()

def GetKeyWords (documents):
    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection (uri)
    body = json.dumps (documents)
    conn.request ("POST", path2, body, headers)
    response = conn.getresponse ()
    return response.read()
tweetlist = []
int x = 1;
while( !Queue.empty() ):
	tweetlist.append({'id': str(x), 'language': 'en', 'text': str(tweet_data.pop())})
documents = { 'doucments': tweetlist }


percentresults = GetSentiment(documents)
keywords = GetKeyWords(documents)
#print(result)


