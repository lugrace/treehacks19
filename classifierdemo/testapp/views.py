import sys
import os
DIR = os.path.dirname(os.path.abspath(__file__))

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

import csv
from google.cloud import vision
from google.cloud.vision import types

from .machine_learning import predictor 
from .machine_learning import classify
from .machine_learning import classify_menu

recognized = set()

with open(r'machine_learning\dictionary.csv', newline='', encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        for element in row:
            recognized.add(element.strip())

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            labels = classify.classify(file)

            is_menu = False
            is_recognized = False
            
            for label in reversed(labels):
                if label.description in recognized:
                    obj = label.description
                    is_recognized = True
                if label.description == 'text':
                    is_menu = True

            if is_menu:
                sorted_food = classify_menu.classify_menu(file)

                # sorted_food is None when the text is small, i.e. not a menu
                if sorted_food is None:
                    # Handle this special case. Shows every single item
                    # return render(...)

            if is_recognized:
                # return render(request, 'result.html', {'result' : obj})
                pass

            # Not correctly recognized by default image => try custom model
            results = predictor.classify_image(file)

            # Note that if picture is something random, classification will be junk
            # ideally ask user if item is correct, and then update model
            obj = results.predictions[0].tag_name
            return render(request, 'result.html', {'result' : obj})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
