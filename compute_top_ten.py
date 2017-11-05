
from tweepy import OAuthHandler
import queue
import tweepy
import http.client
import json

# TWITTER API CREDENTIALS
consumer_key = 'oeaiWzPmHLx20OLsp5g5QPFbw'
consumer_secret = '3b55vyoax4DIkhvTX6KUGP9sSjhxo9ZxOfpUUtsz6tpPVfZfw3'
access_token = '926830219356340225-z2qjfLCagnxp99AL4UhzQ94LUQbo9RR'
access_secret = 'uX5IWIi0ERKLySSQEYIVOSIcjEuHCmJlPwEK2zSLLLgGk'

# acronym dictionary

f = open("college_acronyms.txt", 'r')
colleges = {}
top_ten = {}
line = f.readline()
while line != "":
    line = line.split(' - ')
    fullname = line[1][:-1].split(', ')
    for x in fullname:
        colleges[x] = line[0]
    line = f.readline()


for input_word in colleges:
    acronym_word = colleges[input_word]
    tweet_data = queue.Queue()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    for tweet in tweepy.Cursor(api.search, q=input_word, count=100, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
        #print(tweet.text)
        tweet_data.put(tweet.text)
    for tweet in tweepy.Cursor(api.search, q=acronym_word, count=100, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
        #print(tweet.text)
        tweet_data.put(tweet.text)
    #---
    #analyzing tweets
    accessKey = 'f15920f0f61947c29e12c7f1f12174f9'
    uri = 'westcentralus.api.cognitive.microsoft.com'
    path = '/text/analytics/v2.0/sentiment'
    path2 = '/text/analytics/v2.0/keyPhrases'

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

    x = 1
    while tweet_data.empty() == False:
        tweetlist.append({'id': str(x), 'language': 'en', 'text': str(tweet_data.get())})
        x+=1
    documents = { 'documents': tweetlist }

    percentresults = eval(GetSentiment(documents))
    avpercent = 0.0
    avpercent = avpercent/len(percentresults["documents"])
    top_ten.update({input_word: avpercent})
   # print(avpercent, negative, positive)


import operator
sorted_x = sorted(top_ten.items(), key=operator.itemgetter(1))


returnme = []
for rrr in sorted_x.keys()[0:10]:
    returnme.append(rrr)
    returnme.append(sorted_x[rrr])


print(returnme)
