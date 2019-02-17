from django.conf.urls import url
from django.urls import path
import os
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(DIR, r"vision/treehacks-food-recognizer-3787a7fb5f64.json")

from . import views

urlpatterns = [
    url(r'^home/$', views.index, name='index'),
    url(r'^home/finder/$', views.analyzeForm), #finder
    url(r'^home/college/(?P<college>\w+)/$', views.analyze),
    url(r'^home/college/$', views.analyzeForm),
    url(r'^home/ten/$', views.topTen),
    # url(r'^home/finder/webcam/$', views.webcam),
    url(r'^home/finder/webcam/$', views.webcam_upload_file, name='webcam_upload_file'),
    # url(r'^home/finder/upload/$', views.upload),
    url(r'^home/finder/upload/$', views.upload_file, name='upload_file'),
    url(r'^home/finder/webcam/screenshot/$', views.upload_file_screenshot, name='upload_file_screenshot'),
    # path('', views.upload_file, name='upload_file'),
]
