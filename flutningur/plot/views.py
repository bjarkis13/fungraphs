from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population
import functools
import locale

# Create your views here.

def index(request):
    args = ",".join([str(m.mid) for m in Municipality.objects.filter(mid__isnull=False)])
    return plot(request, args)

def plot(request, args):
    mun_lis = [int(s) for s in args.split(',')]
    print(mun_lis)
    raw = Population.objects.filter(municipality__mid__in=mun_lis).order_by('municipality__name', 'year')
    data = {}
    for line in raw:
        name = line.municipality.name
        if not name in data:
            data[name] = []
        data[name].append((line.year,line.val))
    lis = []
    for key in data:
        lis.append((key, data[key]))
    locale.setlocale(locale.LC_ALL, 'is_IS.UTF-8')
    lis.sort(key=lambda x: functools.cmp_to_key(locale.strcoll)(x[0]))

    template = loader.get_template("plot/logline_plot.html")
    context = RequestContext(request, { 
                'title' : 'Population line plot',
                'plotactive': True,
                'lineplot' : lis,
                'css' : [ "lib/nvd3/build/nv.d3.min.css" ],
                'js': ["lib/d3/d3.min.js", "lib/nvd3/build/nv.d3.min.js" ],
            },
            processors = [])
    return HttpResponse(template.render(context))

def preset(request, group):
    # change group into list of args
    return plot(request, group)

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

