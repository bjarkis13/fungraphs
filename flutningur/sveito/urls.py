from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<mid>[0-9]{4})/$', views.sveito),
]

