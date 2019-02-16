from django.urls import path
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Kevin\AppData\Local\Programs\Python\Python37-32\treehacks\djangotest\testsite\vision\treehacks-food-recognizer-3787a7fb5f64.json"

from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
]