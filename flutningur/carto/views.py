from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population

# Create your views here.

def index(request):
    #raw = Population.objects.filter(year=int(id_year)).filter(municipality__mid__isnull=False).order_by('municipality__name', 'year')
    # if len raw .,
    data = {}
    #for line in raw:
    #    name = line.municipality.name
    #    if not name in data:
    #        data[name] = []
    #    data[name].append((line.municipality.mid,line.val))
    template = loader.get_template("carto/cartogram.html")
    #return HttpResponse("".join(["{}({}):{}, ".format(m.municipality.name, m.year, m.val) for m in data]))
    context = RequestContext(request, { 'data' : data }, processors = [])
    return HttpResponse(template.render())

