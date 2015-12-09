from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population

# Create your views here.

def index(request):
    template = loader.get_template("main_page/home.html")
    context = RequestContext(request, { 'title' : 'beni plz', 'homeactive': True, 'css' : [] }, processors = [])
    return HttpResponse(template.render(context))

