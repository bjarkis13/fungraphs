import os.path
from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
    print(request)
    data = open(os.path.dirname(os.path.abspath(__file__)) + "/templates/population/data").read()
    template = loader.get_template("population/area_line_plot.html")
    context = RequestContext(request, { 'data' : data }, processors = [])
    return HttpResponse(template.render(context))


def index2(request):
    return HttpResponse("Hello, world. You're at the population db")
