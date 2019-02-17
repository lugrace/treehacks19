import sys
import os
DIR = os.path.dirname(os.path.abspath(__file__))

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

import io
from google.cloud import vision
from google.cloud.vision import types

from .machine_learning import predictor 
from .machine_learning import classify
from .machine_learning import classify_menu

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            labels = classify.classify(file)
            obj = labels[0].description
            
            '''
            results = predictor.classify_image(file)
            obj = results.predictions[0].tag_name
            '''
            return render(request, 'result.html', {'result' : obj})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
