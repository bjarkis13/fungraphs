from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population

# Create your views here.

def index(request):
    return HttpResponse("heat map index")

def plot(request, args):
    return HttpResponse("heat map " + args)

def preset(request, group):
    return plot(request, "group" + group)
