from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='gamestore'),
    url(r'^index/$', views.index),
]
