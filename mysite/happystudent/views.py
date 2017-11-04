from django.shortcuts import render
from django.http import HttpResponse

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