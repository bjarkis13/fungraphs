import os.path
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Municipality, Population

def index(request):
    print(request)
    data = open(os.path.dirname(os.path.abspath(__file__)) + "/templates/population/data").read()
    template = loader.get_template("population/area_line_plot.html")
    context = RequestContext(request, { 'data' : data }, processors = [])
    return HttpResponse(template.render(context))

def line(request):
    raw = Population.objects.filter(municipality__mid__isnull=False).order_by('municipality__name', 'year')
    data = {}
    for line in raw:
        name = line.municipality.name
        if not name in data:
            data[name] = []
        data[name].append((line.year,line.val))
    print(data)

    template = loader.get_template("population/area_line_plot2.html")
    #return HttpResponse("".join(["{}({}):{}, ".format(m.municipality.name, m.year, m.val) for m in data]))
    context = RequestContext(request, { 'data' : data }, processors = [])
    return HttpResponse(template.render(context))


def index2(request):
    return HttpResponse("Hello, world. You're at the population db")
