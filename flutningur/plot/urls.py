from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^preset/(?P<group>[0-9]+)/$', views.preset),
    url(r'^(?P<args>[0-9]{4}(,[0-9]{4})*)/$', views.plot),
]

