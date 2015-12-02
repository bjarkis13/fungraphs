#Tilraun til að setja í db

import csv
from population.models import Municipality, Changes, Population

BRPATH = '../data/breytingar.txt'
PATH = '../data/1901-1990.csv'

def getMun(name):
    try:
        mun = Municipality.objects.get(name=name)
    except Municipality.DoesNotExist:
        mun = Municipality(name=name)
        mun.save()
    return mun

def addChanges():
	#Create list of changes
	s = []
	with open(BRPATH) as f:
		for i in f:
			if i == 'Fyrir,Eftir,Ártal\n': continue
			i = i.split(',')
			i[-1] = int(i[-1].strip())
			s.append(i)

	for i in s:
		old = i[0]
		oldMun = getMun(old)
		y = i[-1]
		new = i[1:-1]
		if len(new) > 1:
			for j in new:
				if old == j: continue
				print('Need percent for {}: {}, {}'.format(old,j,y))
				newMun = getMun(j)
				change = Changes(old=oldMun,new=newMun,percent=50,year=y)
				change.save()
		else:
			new = new[0]
			if old == new: print('{} goes into only itself'.format(old))
			newMun = getMun(new)
			newMun.save()
			change = Changes(old=oldMun,new=newMun,percent=100,year=y)
			change.save()
			

def addPopulation():
    with open(PATH) as f:
        reader = csv.reader(f, delimiter=';')
        for i in reader:
            mun = getMun(i[0])
            data = i[1:]
            for y, val in enumerate(data):
                if val == '.' or val == '-': val = 0
                pop = Population(municipality=mun,year=1900+y*10,val=val)
                pop.save()

if __name__ == '__main__':
	addChanges()
