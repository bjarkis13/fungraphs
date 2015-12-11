from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^presentation/$', views.pres),
    url(r'^about/$', views.about),
    url(r'^queries/$', views.queries),
]

