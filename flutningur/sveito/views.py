from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population

# Create your views here.

def index(request):
    return HttpResponse("Sveito index")

def sveito(request, mid):
    try:
        data = {"title" : Municipality.objects.get(mid=int(mid)).name}
    except Municipality.DoesNotExist:
        raise Http404('Municipality does not exist')
    template = loader.get_template("sveito/sveito.html")
    context = RequestContext(request,{"data": data},processors=[])
    return HttpResponse(template.render(context))
