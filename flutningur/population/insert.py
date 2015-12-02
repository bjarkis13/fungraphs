#Tilraun til að setja í db

from django.db import models

BRPATH = '../../data/breytingar.txt'

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
		#automatic id?, do we need change?
		oldMun = Municipality(name=old)
		year = i[-1]
		new = [1:-1]
		for j in new:
			#How do we do this?
			#Splitting % might be warranted
			#Pop val might have to be more soficticated than integers, maybe having error bounds
			if old == j: dostuff()
			newMun = Municipality(name=old)
			change = Changes(old=oldMun,new=newMun,year=year)
			


if __name__ == '__main__':
	addChanges()
