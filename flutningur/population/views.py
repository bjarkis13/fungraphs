from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Municipality, Population

def index(request):
    print(request)
    template = loader.get_template("population/area_line_plot.html")
    context = RequestContext(request, { 'data' : data }, processors = [])
    return HttpResponse(template.render(context))

def lineplot(request):
    raw = Population.objects.filter(municipality__mid__isnull=False).order_by('municipality__name', 'year')
    data = {}
    for line in raw:
        name = line.municipality.name
        if not name in data:
            data[name] = []
        data[name].append((line.year,line.val))

    template = loader.get_template("population/line_plot.html")
    #return HttpResponse("".join(["{}({}):{}, ".format(m.municipality.name, m.year, m.val) for m in data]))
    context = RequestContext(request, { 'data' : data }, processors = [])
    return HttpResponse(template.render(context))

def heatmap(request, id_year="1900"):
    raw = Population.objects.filter(year=int(id_year)).filter(municipality__mid__isnull=False).order_by('municipality__name', 'year')
    # if len raw .,
    data = {}
    for line in raw:
        name = line.municipality.name
        if not name in data:
            data[name] = []
        data[name].append((line.municipality.mid,line.val))
    template = loader.get_template("population/heatmap.html")
    #return HttpResponse("".join(["{}({}):{}, ".format(m.municipality.name, m.year, m.val) for m in data]))
    context = RequestContext(request, { 'data' : raw }, processors = [])
    return HttpResponse(template.render(context))
