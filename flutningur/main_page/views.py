from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population, Regions, SpendingPerCapita

# Create your views here.

def index(request):
    template = loader.get_template("main_page/home.html")
    context = RequestContext(request, {
        'title' : 'Migration within Iceland',
        'homeactive': True,
        'css' : []
        }, processors = [])
    return HttpResponse(template.render(context))

def pres(request):
    template = loader.get_template("main_page/pres.html")

    context = RequestContext(request, { 
        'title' : 'Presentation',
        'presactive': True,
        'css' : [],
        #'js' : ['lib/d3/d3.min.js'],
        }, processors = [])
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template("main_page/about.html")
    context = RequestContext(request, { 
        'title' : 'About us',
        'aboutactive': True,
        'css' : []
        }, processors = [])
    return HttpResponse(template.render(context))

def queries(request):
    template = loader.get_template("main_page/queries.html")
    context = RequestContext(request, { 
        'title' : 'Navigation',
        'queryactive': True,
        'css' : []
        }, processors = [])
    return HttpResponse(template.render(context))
