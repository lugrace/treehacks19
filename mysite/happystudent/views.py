import sys
import base64
from django.core.files.base import ContentFile

import os
import re
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(os.path.join(DIR, r"vision/treehacks-food-recognizer-3787a7fb5f64.json"))

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
from django.shortcuts import render
from .forms import UploadFileForm
import simplejson

import io
from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

# import os

# from wordcloud import WordCloud
# import matplotlib.pyplot as plt

#Variables that contains the user credentials to access Twitter API
# consumer_key = 'oeaiWzPmHLx20OLsp5g5QPFbw'
# consumer_secret = '3b55vyoax4DIkhvTX6KUGP9sSjhxo9ZxOfpUUtsz6tpPVfZfw3'
# access_token = '926830219356340225-z2qjfLCagnxp99AL4UhzQ94LUQbo9RR'
# access_secret = 'uX5IWIi0ERKLySSQEYIVOSIcjEuHCmJlPwEK2zSLLLgGk'

consumer_key = 'nZLGMLHWqqRdXZLJyRO4Aa73i'
consumer_secret = 'S6z8cMV3o1e8Pd1RV7w57KTUloL3XwZGPj9nX885CcE33o36En'
access_token = '1499540593-1EwsHUl4V7gaa1EFXTlqqq5mAceIwsJ3sioQ0Nf'
access_secret = 'BrgR0qv32GbIQQD8fYKXHtcxigrvh4fJJ3Td3LdQEU4tq'

# consumer_key = 'USKNo3FUPLEY4Drk7PGOP3vfs'
# consumer_secret = 'EexUTxb2MDYQw51jz9xYaB3eFv9uMd2CdIdWzxNY8OeX0m05to'
# access_token = '927051697876324352-3Vqh7zQybwZPu7VGggnLc4MBwbeoZTT'
# access_secret = 'kHVihIkPLvud5p0665ceKHcrLq2qrTl4yinnD5tV0X1oj'

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


def analyze(request, college="University of Maryland"):
	#do stuff
	f = open("static/txt/college_acronyms.txt", 'r', encoding="utf8")
	colleges = {}
	line = f.readline()
	while line != "":
	    line = line.split(' - ')
	    fullname = line[1][:-1].split(', ')
	    for x in fullname:
	        colleges[x] = line[0]
	    line = f.readline()

	input_word = college
	if input_word in colleges.keys():
		acronym_word = colleges[input_word]
	else:
		acronym_word = college.replace("University", "")
		acronym_word = college.replace("College of", "")
		acronym_word = college.replace("College", "")
		acronym_word.strip()
	tweet_data = queue.Queue()

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	for tweet in tweepy.Cursor(api.search, q=input_word, count=3500, result_type="recent", include_entities=True, lang="en").items(200):     # the values inside items defines how many searches we want
	    #print(tweet.text)
	    if( not tweet.retweeted):
	    	tweet_data.put(tweet.text)
	for tweet in tweepy.Cursor(api.search, q=acronym_word, count=3500, result_type="recent", include_entities=True, lang="en").items(200):     # the values inside items defines how many searches we want
	    #print(tweet.text)
	    if (not tweet.retweeted):
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
	sortnums = []
	for z in percentresults["documents"]:
		avpercent += z["score"]
		sortnums.append([z["score"], z['id']])
		if z["score"] < 0.01:
			negative+=1
		elif z["score"] > 0.8:
			positive+=1
	sortnums = sorted(sortnums)
	examplebad = []
	index = 0
	count = 0
	examplegood = []
	while count < 3:
		tw = tweetlist[int(sortnums[index][1])-1]['text']
		if tw not in examplebad:
			if ("RT @" not in tw) and ("http" not in tw) and ("trump" not in tw.lower()) and ("lyft" not in tw.lower()):
				examplebad.append(tw)
				count+=1
		index+=1
	index = -1
	count = 0
	while count < 3:
		tw = tweetlist[int(sortnums[index][1])-1]['text']
		if tw not in examplegood:
			if ("RT @" not in tw) and ("http" not in tw) and ("trump" not in tw.lower()) and ("lyft" not in tw.lower()):
				examplegood.append(tw)
				count+=1
		index-=1
	#examplegood = [tweetlist[int(sortnums[-1][1])-1]['text'], tweetlist[int(sortnums[-2][1])-1]['text'], tweetlist[int(sortnums[-3][1])-1]['text']]
	avpercent = avpercent/len(percentresults["documents"])
	negative = negative/len(percentresults["documents"])
	positive = positive/len(percentresults["documents"])

	avpercentR = int(int(avpercent*100)/100*100)
	negativeR = int(int(negative*100)/100*100)
	positiveR = int(int(positive*100)/100*100)

	# wordle stuff
	# words = [
			# {text: "Lorem", weight: 15},
			# {text: "Ipsum", weight: 9, link: "http://jquery.com/"},
			# {text: "Dolor", weight: 6, html: {title: "I can haz any html attribute"}},
			# {text: "Sit", weight: 7},
			# {text: "Amet", weight: 5}
 #	];
	wordqueue = queue.Queue()
	keywords = eval(GetKeyWords(documents))
	badfile = open("static/txt/badfile.txt", 'r', encoding="utf8")
	badline = badfile.readline()
	badwords = {}
	while badline != "":
		badline.strip()
		badline = badline[:-1].lower()
		badwords[badline] = 0
		badline = badfile.readline()
	goodfile = open("static/txt/goodfile.txt", 'r', encoding="utf8")
	goodline = goodfile.readline()
	goodwords = {}
	while goodline != "":
		goodline.strip()
		goodline = goodline[:-1].lower()
		goodwords[goodline] = 0
		goodline = goodfile.readline()
	for w in keywords["documents"]:
		for wordphrase in w["keyPhrases"]:
			for word in wordphrase.split(" "):
				wordqueue.put(word.lower())

	while wordqueue.empty() != True:
		inbad = False
		findword = wordqueue.get()
		for x in badwords.keys():
			if x == findword[:len(x)]:
				badwords[x] +=1
				inbad = True
				break
		if inbad != True:
			for x in goodwords.keys():
				if x == findword[:len(x)]:
					goodwords[x] +=1
					break
	badstringinput = ""
	for x in badwords.keys():
		badstringinput += (x+" ")*badwords[x]
	badstringinput.strip()
	goodstringinput = ""
	for x in goodwords.keys():
		goodstringinput += (x+" ")*goodwords[x]
	goodstringinput.strip()
	badstringinput = badstringinput.split(" ")
	goodstringinput = goodstringinput.split(" ")
	# words = ["fuck", "wtf"]
	# json_list = simplejson.dumps(words)
	# words = badstringinput.concat(goodstringinput)
	words = badstringinput + goodstringinput
	words_list = simplejson.dumps(words)
	# badwords_list = simplejson.dumps(badstringinput)
	# goodwords_list = simplejson.dumps(goodstringinput)

	return render(
		request, 
		'results.html',
		context={'college_name':college, 'avpercent': avpercentR, 'positive': positiveR, 'negative': negativeR, 
		'exampleGood1': examplegood[0], 'exampleGood2': examplegood[1], 'exampleGood3': examplegood[2], 
		'exampleBad1': examplebad[0], 'exampleBad2': examplebad[1], 'exampleBad3': examplebad[2],
		'words': words_list}
		# 'words': json_list
	)

def analyzeForm(request):
	if request.method == 'POST':
		form = CollegeForm(request.POST)
		if form.is_valid():
			return analyze(request, form.cleaned_data['your_college'])
	else:
		form = CollegeForm()

	return render(request, 'finder.html', {'form': form})


def finder(request):
	#do stuff
	return render(
		request,
		'finder.html',
	)

def webcam(request):
	#do stuff
	return render(
		request,
		'webcam.html',
	)

def upload(request):
	#do stuff
	return render(
		request,
		'upload.html',
	)

def classify(image_file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(DIR, r"vision/treehacks-food-recognizer-3787a7fb5f64.json")

    content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    return labels

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            labels = classify(file)
            obj = labels[0].description

            return render(request, 'results.html', {'result' : obj})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def upload_file_screenshot(request):
    if request.method == 'POST':
        # form = UploadFileScreenshotForm(request.POST, request.FILES)
        # if form.is_valid():
        #     file = request.FILES['file']
        #     labels = classify(file)
        #     obj = labels[0].description
        file = request.FILES['img_data']#['img_data']['name']#['img_data']
        labels = classify(file)
        obj = labels[0].description

        return render(request, 'results.html', {'result' : obj}) #used to be indented
    else:
        form = UploadFileScreenshotForm()
    return render(request, 'webcam.html', {'form': form})

def webcam_upload_file(request):
    if request.method == 'POST':
        form = CollegeForm(request.POST, request.FILES)
        if form.is_valid():
            # dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
            # image_data = cleaned_data['image_data']
            # image_data = dataUrlPattern.match(image_data).group(2)
            # image_data = image_data.encode()
            # image_data = base64.b64decode(image_data)
            image_data = request['user']['image']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))  
            file = data#request.FILES['file']
            labels = classify(file)
            obj = labels[0].description

            return render(request, 'results.html', {'result' : obj})
    else:
        form = CollegeForm()
    return render(request, 'webcam.html', {'form': form})


def get_college(request):
	if request.method == 'POST':
		form = CollegeForm(request.POST)
		if form.is_valid():
			return analyze(request, form.your_college)
	else:
		form = CollegeForm()

	return render(request, 'results.html', {'form': form})


def topTen(request):
	# f = open("static/txt/college_acronyms.txt", 'r', encoding="utf8")
	# colleges = {}
	# top_ten = {}
	# line = f.readline()
	# while line != "":
	#     line = line.split(' - ')
	#     fullname = line[1][:-1].split(', ')
	#     for x in fullname:
	#         colleges[x] = line[0]
	#     line = f.readline()

	# for input_word in colleges:
	#     acronym_word = colleges[input_word]
	#     tweet_data = queue.Queue()

	#     auth = OAuthHandler(consumer_key, consumer_secret)
	#     auth.set_access_token(access_token, access_secret)
	#     api = tweepy.API(auth)

	#     for tweet in tweepy.Cursor(api.search, q=input_word, count=3500, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
	#         tweet_data.put(tweet.text)
	#     for tweet in tweepy.Cursor(api.search, q=acronym_word, count=3500, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
	#         tweet_data.put(tweet.text)
	#     tweetlist = []

	#     x = 1
	#     while tweet_data.empty() == False:
	#         tweetlist.append({'id': str(x), 'language': 'en', 'text': str(tweet_data.get())})
	#         x+=1
	#     documents = { 'documents': tweetlist }

	#     percentresults = eval(GetSentiment(documents))
	#     avpercent = 0.0
	#     positive = 0.0
	#     negative = 0.0
	#     for z in percentresults["documents"]:
	#         avpercent += z["score"]
	#         if z["score"] < 0.01:
	#             negative+=1
	#         elif z["score"] > 0.8:
	#             positive+=1
	#     avpercent = avpercent/len(percentresults["documents"])
	#     top_ten.update({input_word: avpercent})
	# sorted_x = sorted(top_ten.items(), key=operator.itemgetter(1))

	# returnme = []
	# for rrr in sorted_x.keys()[0:10]:
	# 	returnme.append(rrr)
	# 	returnme.append(sorted_x[rrr])

	return render(
		request, 
		'ten.html',
		# context={'returnme': returnme}
	)
