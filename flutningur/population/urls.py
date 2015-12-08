from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.heatmap),
    url(r'^(?P<id_year>[0-9]{4})/$', views.heatmap),
]

