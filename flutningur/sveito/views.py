from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population

# Create your views here.

def index(request):
    return HttpResponse("Sveito index")

def sveito(request, mid):
    return HttpResponse("Sveito nr " + args)
