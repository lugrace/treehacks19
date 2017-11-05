from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

#for the backend part
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import queue
import tweepy

import http.client
import json

import operator

#for forms
from .forms import CollegeForm

#Variables that contains the user credentials to access Twitter API
# consumer_key = 'oeaiWzPmHLx20OLsp5g5QPFbw'
# consumer_secret = '3b55vyoax4DIkhvTX6KUGP9sSjhxo9ZxOfpUUtsz6tpPVfZfw3'
# access_token = '926830219356340225-z2qjfLCagnxp99AL4UhzQ94LUQbo9RR'
# access_secret = 'uX5IWIi0ERKLySSQEYIVOSIcjEuHCmJlPwEK2zSLLLgGk'

consumer_key = 'nZLGMLHWqqRdXZLJyRO4Aa73i'
consumer_secret = 'S6z8cMV3o1e8Pd1RV7w57KTUloL3XwZGPj9nX885CcE33o36En'
access_token = '1499540593-1EwsHUl4V7gaa1EFXTlqqq5mAceIwsJ3sioQ0Nf'
access_secret = 'BrgR0qv32GbIQQD8fYKXHtcxigrvh4fJJ3Td3LdQEU4tq'

#analyzing tweets
accessKey = 'f15920f0f61947c29e12c7f1f12174f9'
uri = 'westcentralus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'
path2 = '/text/analytics/v2.0/keyPhrases'

# Create your views here.
def index(request):
	return render(
        request,
        'index.html'
    )
    # return HttpResponse("Hello, world. You're at the polls index.")

def analyze(request, college="University of Maryland"):
	#do stuff
	f = open("static/txt/college_acronyms.txt", 'r', encoding="utf8")
	colleges = {}
	line = f.readline()
	while line != "":
	    line = line.split(' - ')
	    fullname = line[1].split(', ')[:-1]
	    for x in fullname:
	        colleges[x] = line[0]
	    line = f.readline()

	input_word = college
	acronym_word = colleges[input_word]
	tweet_data = queue.Queue()

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	for tweet in tweepy.Cursor(api.search, q=input_word, count=3500, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
	    #print(tweet.text)
	    tweet_data.put(tweet.text)
	for tweet in tweepy.Cursor(api.search, q=acronym_word, count=3500, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
	    #print(tweet.text)
	    tweet_data.put(tweet.text)

	tweetlist = []

	x = 1
	while tweet_data.empty() == False:
	    tweetlist.append({'id': str(x), 'language': 'en', 'text': str(tweet_data.get())})
	    x+=1
	documents = { 'documents': tweetlist }

	percentresults = eval(GetSentiment(documents))
	avpercent = 0.0
	positive = 0.0
	negative = 0.0
	for z in percentresults["documents"]:
	    avpercent += z["score"]
	    if z["score"] < 0.01:
	        negative+=1
	    elif z["score"] > 0.8:
	        positive+=1
	avpercent = avpercent/len(percentresults["documents"])
	negative = negative/len(percentresults["documents"])
	positive = positive/len(percentresults["documents"])

	avpercentR = int(int(avpercent*100)/100*100)

	return render(
		request, 
		'results.html',
		context={'college_name':college, 'avpercent': avpercentR}
	)

def analyzeForm(request):
	if request.method == 'POST':
		form = CollegeForm(request.POST)
		if form.is_valid():
			return analyze(request, form.cleaned_data['your_college'])
	else:
		form = CollegeForm()

	return render(request, 'finder.html', {'form': form})

def topten(request):
	#do stuff
	return render(
		request,
		'ten.html'
	)

def finder(request):
	#do stuff
	return render(
		request,
		'finder.html',
	)

def get_college(request):
	if request.method == 'POST':
		form = CollegeForm(request.POST)
		if form.is_valid():
			return analyze(request, form.your_college)
	else:
		form = CollegeForm()

	return render(request, 'results.html', {'form': form})

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

def topTen(request):
	f = open("static/txt/college_acronyms.txt", 'r', encoding="utf8")
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

	    for tweet in tweepy.Cursor(api.search, q=input_word, count=3500, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
	        tweet_data.put(tweet.text)
	    for tweet in tweepy.Cursor(api.search, q=acronym_word, count=3500, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
	        tweet_data.put(tweet.text)
	    tweetlist = []

	    x = 1
	    while tweet_data.empty() == False:
	        tweetlist.append({'id': str(x), 'language': 'en', 'text': str(tweet_data.get())})
	        x+=1
	    documents = { 'documents': tweetlist }

	    percentresults = eval(GetSentiment(documents))
	    avpercent = 0.0
	    positive = 0.0
	    negative = 0.0
	    for z in percentresults["documents"]:
	        avpercent += z["score"]
	        if z["score"] < 0.01:
	            negative+=1
	        elif z["score"] > 0.8:
	            positive+=1
	    avpercent = avpercent/len(percentresults["documents"])
	    top_ten.update({input_word: avpercent})
	sorted_x = sorted(top_ten.items(), key=operator.itemgetter(1))

	returnme = []
	for rrr in sorted_x.keys()[0:10]:
		returnme.append(rrr)
		returnme.append(sorted_x[rrr])

	return render(
		request, 
		'results.html',
		context={'returnme': returnme}
	)