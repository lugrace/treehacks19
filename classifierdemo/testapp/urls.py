from django.urls import path
import os
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(DIR))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, r"auth\treehacks-food-recognizer-3787a7fb5f64.json")

from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
]