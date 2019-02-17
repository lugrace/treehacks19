import sys
import os
DIR = os.path.dirname(os.path.abspath(__file__))
print(os.path.join(DIR, r"vision\treehacks-food-recognizer-3787a7fb5f64.json"))

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

import io
from google.cloud import vision
from google.cloud.vision import types

from . import predictor 

def classify(image_file):
    client = vision.ImageAnnotatorClient()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(DIR, r"vision\treehacks-food-recognizer-3787a7fb5f64.json")

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
            
            '''
            labels = classify(file)
            obj = labels[0].description
            '''

            results = predictor.classify_image(file)
            obj = results.predictions[0].tag_name

            return render(request, 'result.html', {'result' : obj})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
