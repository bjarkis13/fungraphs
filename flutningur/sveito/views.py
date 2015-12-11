from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population, GenderPop

# Create your views here.

def index(request):
    template = loader.get_template("sveito/index.html")
    raw = Municipality.objects.filter(mid__isnull=False).order_by('region__name','name')
    data = {}
    for obj in raw:
        if obj.region.name not in data:
            data[obj.region.name] = []
        data[obj.region.name].append((obj.name, obj.mid))
    context = RequestContext(request, { 
            'title' : 'Municipalities',
            'sveitoactive': True,
            'css' : ["mystyle.css"],
            'regions' : data,
            'js':["jquery-1.10.2.min.js", "d3.v2.min.js"]
        }, processors = [])
    return HttpResponse(template.render(context))


def sveito(request, mid):
    try:
        data = {"title" : Municipality.objects.get(mid=int(mid)).name}
    except Municipality.DoesNotExist:
        raise Http404('Municipality does not exist')

    #Year is temporarily hardcoded
    year = 2014
    #We create the data for population pyramids
    data["gpop"] = []
    gpop = GenderPop.objects.filter(municipality__mid=int(mid),year=year)
    for i in gpop:
        data["gpop"].append([i.ageclass,i.valm,i.valf,i.year])

    #Add the data from total iceland
    data["allgpop"] = []
    gpop = GenderPop.objects.filter(municipality__name="Alls",year=year)
    for i in gpop:
        data["allgpop"].append([i.ageclass,i.valm,i.valf,i.year])


    data["sveitoactive"] = True
    data["js"] = ['lib/d3/d3.min.js']
    template = loader.get_template("sveito/sveito.html")
    context = RequestContext(request,data,processors=[])
    return HttpResponse(template.render(context))
