from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from population.models import Municipality, Population, GenderPop

# Create your views here.

def index(request):
	return HttpResponse("Sveito index")

def sveito(request, mid):
	try:
		data = {"title" : Municipality.objects.get(mid=int(mid)).name}
	except Municipality.DoesNotExist:
		raise Http404('Municipality does not exist')

	#Year is temporarily hardcoded
	#Create a dictionary for age ranges
	popdic = {20:'100+'}
	for i in range(20):
		popdic[i] = '{}-{}'.format(i*5,i*5+4)

	#We create the data for population pyramids
	data["gpop"] = []
	gpop = GenderPop.objects.filter(municipality__mid=int(mid),year=2010)
	for i in gpop:
		data["gpop"].append([popdic[i.ageclass],i.valm,i.valf])

	template = loader.get_template("sveito/sveito.html")
	context = RequestContext(request,data,processors=[])
	return HttpResponse(template.render(context))
