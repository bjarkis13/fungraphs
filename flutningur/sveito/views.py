from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population, GenderPop, Regions, SpendingPerCapita

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
        mun = Municipality.objects.get(mid=int(mid)).name
    except Municipality.DoesNotExist:
        raise Http404('Municipality does not exist')

    #Year is temporarily hardcoded
    year = 2014
    #Create the data for population pyramids
    gpop = []
    gpop_obj = GenderPop.objects.filter(municipality__mid=int(mid),year=year)
    for i in gpop_obj:
        gpop.append([i.ageclass,i.valm,i.valf,i.year])

    #Add the data from total iceland
    gpop_all = []
    gpop_obj = GenderPop.objects.filter(municipality__name="Alls",year=year)
    for i in gpop_obj:
        gpop_all.append([i.ageclass,i.valm,i.valf,i.year])


    #Add the data for spending
    for i in Regions.objects.all():
        if i.low <= int(mid) <= i.high:
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
            s.append((getattr(model,field)/1000,model.name))
        spending.append(s)

    #sorting for consistency
    spending.sort()
    spending = spending[::-1]
 
    template = loader.get_template("sveito/sveito.html")
    context = RequestContext(request, {
    'title' : mun,
    'sveitoactive' : True,
    'js' : ['lib/d3/d3.min.js'],
    'region': reg, 
    'gpop' : gpop,
    'allgpop' : gpop_all,
    'spending' : spending
    },processors=[])
    return HttpResponse(template.render(context))
