import sys
import os
DIR = os.path.dirname(os.path.abspath(__file__))

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm, MultipleUploadFileForm
from django.core.files.storage import default_storage

import csv
from google.cloud import vision
from google.cloud.vision import types

from .util import write_data

from .util.machine_learning import predictor 
from .util.machine_learning import classify
from .util.machine_learning import classify_menu
from .util.machine_learning import trainer

recognized = set()
TRESHOLD = 0.5

with open(r'dictionary.csv', newline='', encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        for element in row:
            recognized.add(element.strip().lower())

def convert_file(img_file, tmp_filename):
    '''
    Converts from InMemoryUploadedFile to a python File
    '''
    with default_storage.open(tmp_filename, 'wb+') as destination:
        for chunk in img_file.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            labels = classify.classify(file)

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
            
            if is_menu:
                convert_file(file, 'tmp/temp2.txt')
                f = open('tmp/temp2.txt', 'rb')
                sorted_food = classify_menu.classify_menu(f)

                # sorted_food is None when the text is small, i.e. not a menu
                if sorted_food is not None:
                    # Handle this special case. Shows every single item
                    # return render(...)
                    return render(request, 'result.html', {'result': str(sorted_food)})

            if is_recognized:
                return render(request, 'result.html', {'result' : obj})

            convert_file(file, 'tmp/temp.txt')

            # Not correctly recognized by default image => try custom model    
            f = open('tmp/temp.txt', 'rb')
            results = predictor.classify_image(f)

            # Note that if picture is something random, classification will be junk
            # ideally ask user if item is correct, and then update model
            obj = results.predictions[0].tag_name
            if (results.predictions[0].probability < TRESHOLD) or obj == 'none':
                obj = 'Cannot identify image'

            return render(request, 'result.html', {'result' : obj})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

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

            try:
                trainer.delete_all_iterations()
                trainer.train_model()
            except:
                return render(request, 'result.html', {'result': 'error'})
            
    else:
        form = MultipleUploadFileForm()
    return render(request, 'upload.html', {'form': form})
