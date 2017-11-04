from django.shortcuts import render
from django.http import HttpResponse

#for the backend part
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
consumer_key = 'oeaiWzPmHLx20OLsp5g5QPFbw'
consumer_secret = '3b55vyoax4DIkhvTX6KUGP9sSjhxo9ZxOfpUUtsz6tpPVfZfw3'
access_token = '926830219356340225-z2qjfLCagnxp99AL4UhzQ94LUQbo9RR'
access_secret = 'uX5IWIi0ERKLySSQEYIVOSIcjEuHCmJlPwEK2zSLLLgGk'

# Create your views here.
def index(request):
	return render(
        request,
        'index.html'
    )
    # return HttpResponse("Hello, world. You're at the polls index.")

def analyze(request, college="University of Maryland"):
	#do stuff

	return render(
		request, 
		'results.html',
		context={'college_name':college}
	)

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
		'finder.html'
	)