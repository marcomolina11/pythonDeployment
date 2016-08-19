from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.addpage),
    url(r'^registration$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addTrip$', views.addTrip),
    url(r'^destination/(?P<id>\d+)$', views.destination)
]