from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<scale>(?:linear|log))/$', views.scale),
    url(r'^preset/(?P<group>[0-9])/$', views.preset),
    url(r'^(?P<scale>(?:linear|log))/preset/(?P<group>[0-9])/$', views.preset),
    url(r'^(?P<args>[0-9]{4}(,[0-9]{4})*)/$', views.plot),
    url(r'^(?P<scale>(?:linear|log))/(?P<args>[0-9]{4}(,[0-9]{4})*)/$', views.plot),
    url(r'^regions/$', views.plot_regions),
    url(r'^(?P<scale>(?:linear|log))/regions/$', views.plot_regions),
]

