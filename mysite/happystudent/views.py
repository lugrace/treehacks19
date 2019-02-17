import sys
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import pyrebase
import csv

import os
import re
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR2 = os.path.dirname(os.path.abspath(__file__))

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

#for the backend part
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from .machine_learning import predictor 
from .machine_learning.classify import classify
from .machine_learning import classify_menu
from .machine_learning import trainer
from .machine_learning import write_data

import queue
import tweepy

import http.client
import json

import operator

#for forms
from .forms import CollegeForm
from django.shortcuts import render
from .forms import UploadFileForm, MultipleUploadFileForm
import simplejson

import io
from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

consumer_key = 'nZLGMLHWqqRdXZLJyRO4Aa73i'
consumer_secret = 'S6z8cMV3o1e8Pd1RV7w57KTUloL3XwZGPj9nX885CcE33o36En'
access_token = '1499540593-1EwsHUl4V7gaa1EFXTlqqq5mAceIwsJ3sioQ0Nf'
access_secret = 'BrgR0qv32GbIQQD8fYKXHtcxigrvh4fJJ3Td3LdQEU4tq'

#analyzing tweets
accessKey = 'f15920f0f61947c29e12c7f1f12174f9'
uri = 'westcentralus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'
path2 = '/text/analytics/v2.0/keyPhrases'

recognized = set()
TRESHOLD = 0.5

with open(os.path.join(DIR2, r'dictionary.csv'), newline='', encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        for element in row:
            recognized.add(element.strip().lower())

# Create your views here.
def index(request):
	return render(
        request,
        'index.html'
    )

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
	words = badstringinput + goodstringinput
	words_list = simplejson.dumps(words)

	return render(
		request, 
		'results.html',
		context={'college_name':college, 'avpercent': avpercentR, 'positive': positiveR, 'negative': negativeR, 
		'exampleGood1': examplegood[0], 'exampleGood2': examplegood[1], 'exampleGood3': examplegood[2], 
		'exampleBad1': examplebad[0], 'exampleBad2': examplebad[1], 'exampleBad3': examplebad[2],
		'words': words_list}
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

def convert_file(img_file, tmp_filename):
    '''
    Converts from InMemoryUploadedFile to a python File
    '''
    with default_storage.open(tmp_filename, 'wb+') as destination:
        for chunk in img_file.chunks():
            destination.write(chunk)

def upload_file(request):
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         file = request.FILES['file']
    #         labels = classify(file)
    #         obj = labels[0].description

    #         return_values = get_info([obj])

    #         # return render(request, 'results.html', {'result' : obj})
    #         return render(request, 'results.html', {'result':obj, 'land' : str(return_values[0][0])[0:4], 'co2':return_values[0][1], 'water': return_values[0][2]})
    # else:
    #     form = UploadFileForm()
    # return render(request, 'upload.html', {'form': form})
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            labels = classify(file)

            is_menu = False
            is_recognized = False
            
            obj = None
            for label in reversed(labels):
                desc = label.description.lower()
                if desc in recognized:
                    obj = label.description
                    is_recognized = True
                if desc in ['text', 'menu']:
                    is_menu = True
            
            if is_menu: #special
                convert_file(file, 'tmp/temp2.txt')
                f = open('tmp/temp2.txt', 'rb')

                sorted_food = classify_menu.classify_menu(f)

                # sorted_food is None when the text is small, i.e. not a menu
                if sorted_food is not None:
                    # Handle this special case. Shows every single item
                    # return render(...)
                    # return render(request, 'results.html', {'result': str(sorted_food)})
                    sortedfood2 = []
                    for next in sorted_food:
                    	word = ""
                    	for words in next[1]:
                    		if("$" not in words):
                    			word = word + " " + words
                    	sortedfood2.append([word.strip().lower().capitalize(), str(next[2])[0:4]])
                    return render(request, 'results-menu.html', {'menu': 'yes', 'result': sortedfood2})

            if is_recognized:
                # return render(request, 'results.html', {'result' : obj})
                return_values = get_info([obj])
                # return render(request, 'results.html', {'result':obj, 'land' : str(return_values[0][0])[0:4], \
                # 	'co2':return_values[0][1], 'water': return_values[0][2]})
                print(return_values)
                return render(request, 'results.html', {'result':obj, 'land' : str(return_values[0][2])[0:4], \
            	'co2':str(return_values[0][0])[0:4], 'water': str(return_values[0][1])[0:4], \
            	'land2' : str(return_values[1][2])[0:4], \
            	'co22':str(return_values[1][0])[0:4], 'water2': str(return_values[1][1])[0:4]})


            convert_file(file, 'tmp/temp.txt')

            # Not correctly recognized by default image => try custom model    
            f = open('tmp/temp.txt', 'rb')
            
            results = predictor.classify_image(f)

            print("RESULTS", results)

            # Note that if picture is something random, classification will be junk
            # ideally ask user if item is correct, and then update model
            obj = results.predictions[0].tag_name
            return_values = get_info([obj])

            print('RETVALUES', return_values)

            # return render(request, 'results.html', {'result' : obj})
            return render(request, 'results.html', {'result':obj, 'land' : str(return_values[0][2])[0:4], \
            	'co2':str(return_values[0][0])[0:4], 'water': str(return_values[0][1])[0:4], \
            	'land2' : str(return_values[1][2])[0:4], \
            	'co22':str(return_values[1][0])[0:4], 'water2': str(return_values[1][1])[0:4]})
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
    return render(request, 'webcam.html')

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
    # else:
    #     form = CollegeForm()
    return render(request, 'webcam.html')


def get_college(request):
	if request.method == 'POST':
		form = CollegeForm(request.POST)
		if form.is_valid():
			return analyze(request, form.your_college)
	else:
		form = CollegeForm()

	return render(request, 'results.html', {'form': form})

def get_info(list_of_words):
    
    list_of_words = [x.lower() for x in list_of_words]
    co2, water, land, co2_score, water_score, land_score = 0, 0, 0, 0, 0, 0;


    #get stats from firebase
    config = {
        "apiKey": "R0j6JfG91yeNdN1QZDPufpClbAMB5STTx2X4Z3L1",
        "authDomain": "treehacks-3750e.firebaseapp.com",
        "databaseURL": "https://treehacks-3750e.firebaseio.com",
        "storageBucket": "treehacks-3750e.appspot.com",
        "serviceAccount": "firebase_cred.json"
        }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()


    # get words and categories
    with open(os.path.join(DIR2, r'dictionary.csv'), newline='', encoding='utf-8', errors='ignore') as csvfile:
            data = list(csv.reader(csvfile))
            
    new_data = [];

    for x in data:
        temp = [];
        for j in x:
            if (j != ''):
                temp.append(j.lower())
        new_data.append(temp)
        
    data = new_data
    counter = 1;

    #check if each word is in a category, and increment the values if so
    for word in list_of_words:
        for x in data:
            if word in x:
                ind = data.index(x)
                category = data[ind][0].replace(" ", "")
                ghg = db.child(category).child("GHG").get().val()
                landUse = db.child(category).child("landUse").get().val()
                h2o = db.child(category).child("water").get().val()
                co2 = co2 + ghg
                water = water + h2o
                land = land + landUse
                co2_score = co2_score + (1/counter) * db.child(category).child("GHGscore").get().val() #weigh based on certainty/importance
                water_score = water_score + (1/counter) *db.child(category).child("waterscore").get().val()
                land_score = land_score + (1/counter) * db.child(category).child("landscore").get().val()
                counter = counter + 1;
                data.remove(x); #prevent double-counting an item
                break;


    return [[co2, water, land], [co2_score, water_score, land_score]]

def upload_training_files(request):
    if request.method == 'POST':
        form = MultipleUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')

            to_add = []
            tag = request.POST['name']

            co2 = request.POST['co2']
            land_use = request.POST['land_use']
            water_use = request.POST['water_use']
            
            for file in files:
                convert_file(file, 'tmp/temp3.txt')
                f = open('tmp/temp3.txt', 'rb')
                write_data.write_data(tag, water_use, co2, land_use)
                trainer.add_training_image(f, tag)

            # try:
            trainer.delete_all_iterations()
            trainer.train_model()

            # except:
            #     return render(request, 'results.html', {'result': 'error'})
            
    else:
        form = MultipleUploadFileForm()
    return render(request, 'upload.html', {'form': form})


def topTen(request):
	return render(
		request, 
		'ten.html',
		# context={'returnme': returnme}
	)
