from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population

# Create your views here.

def index(request):
    return HttpResponse(request)

def plot(request, args):
    return HttpResponse(args)

def preset(request, group):
    # change group into list of args
    return plot(request, group)
