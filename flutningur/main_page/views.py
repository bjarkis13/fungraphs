from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population, Regions, SpendingPerCapita

# Create your views here.

def index(request):
    template = loader.get_template("main_page/home.html")
    context = RequestContext(request, { 'title' : 'beni plz', 'homeactive': True, 'css' : [] }, processors = [])
    return HttpResponse(template.render(context))

def pres(request):
    template = loader.get_template("main_page/pres.html")

    #Here we need to know what sveito it is for now let's choose one
    mid = 8000
    
    mun = Municipality.objects.get(mid=8000).name
    for i in Regions.objects.all():
        if i.low < mid < i.high:
            reg = i.name
            break

    names = ['Alls','good','bad',mun,reg]
    indnames = [(i,i) for i in names] 
    spending = []
    toPlot = [SpendingPerCapita.objects.get(name=i) for i in names]
 
    field_names = toPlot[0]._meta.get_all_field_names()


    for field in field_names:
        if field == 'name' or field == 'id' or field == 'income' or field == 'health': continue
        s = [(field,'Sveito')]
        for model in toPlot:
            s.append((getattr(model,field),model.name))
        spending.append(s)

    #sorting for consistency
    spending.sort()

    context = RequestContext(request, { 
        'title' : 'Presentation',
        'presactive': True,
        'css' : [],
        'js' : ['lib/d3/d3.min.js'],
        'spending' : spending
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
