from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/$', views.index, name='index'),
    url(r'^home/finder/$', views.analyzeForm), #finder
    url(r'^home/college/(?P<college>\w+)/$', views.analyze),
    url(r'^home/college/$', views.analyzeForm),
    url(r'^home/ten/$', views.topTen),
]
