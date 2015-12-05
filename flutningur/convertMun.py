#FUCK THIS SHIT
from population.models import Municipality, Changes, Population

def getChanges(year, toYear=2015, verbose=False):
    s = []
    last = 0
    for i in Changes.objects.all():
        #print(i.old.name,i.new.name,i.percent,i.year)
        if i.year < last:
            print('Change list is not sorted!')
            break
        last = i.year

        if i.year < year: continue
        if i.year >= toYear: break

        try:
            opop = Population.objects.get(municipality=i.old,year=year)
        #print(opop.municipality.name, opop.val)
        except Population.DoesNotExist:
            continue
        try:
            npop = Population.objects.get(municipality=i.new,year=year)
        except Population.DoesNotExist:
            print('Created value for {} at {}'.format(i.new.name,year))
            npop = Population(municipality=i.new,year=year,val=0)

        
        update = int(opop.val * (i.percent/100.0))
        opop.val -= update
        npop.val += update
        opop.save()
        npop.save()
        
        if verbose: print('Moved {} people from {} to {}'.format(update, opop.municipality.name, npop.municipality.name))


def updateAll():
    years = range(1900,1991,10)
    for i in years:
        getChanges(i)

