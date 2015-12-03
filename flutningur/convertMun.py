#FUCK THIS SHIT
from population.models import Municipality, Changes, Population

def getChanges(year, toYear=2015):
    s = []
    for i in Changes.objects.all():
        #print(i.old.name,i.new.name,i.percent,i.year)
        try:
            opop = Population.objects.get(municipality=i.old,year=year)
        #print(opop.municipality.name, opop.val)
        except Population.DoesNotExist:
            print(i.old.name)
