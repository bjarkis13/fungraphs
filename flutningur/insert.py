#!/usr/bin/env python3
import csv
import os.path
from django.db import IntegrityError, transaction
from population.models import Municipality, Changes, Population, GenderPop, Regions, SpendingPerCapita, Education

BRPATH = 'breytingar.txt'
PCPATH = 'skiptingar.csv'
DPATH = '../data'
MIDPATH = 'sveitarfelog.txt'
GPATH = 'mannfjoldi98-15.csv'
SVEITOPATH = 'sveitarfelog.txt'
REGIONPATH = 'landshlutar.csv'
SPENDPATH = 'saga/framlog2014.csv'
EDUPATH = 'saga/menntamal.csv'
GROUPPATH = 'flokkar.txt'
ID = {}
REGIONS = []
GROUPDATA = {}

def getRegion(mid):
    if mid is None:
        return None
    for R in REGIONS:
        if R.low <= mid and mid <= R.high:
            return R
    print('Error region for {} not found'.format(mid))
    return None

def listMun():
    s = []
    with open(os.path.join(DPATH,SVEITOPATH)) as f:
        for i in f:
            s.append(i.strip().split(',')[1])
    return s

def getGroups():
    ret = []
    group = []
    with open(os.path.join(DPATH,GROUPPATH)) as f:
        for i in f:
            i = i.strip()
            if i[-1] == ':':
                if group != []: ret.append(group)
                group = []
            else:
                group.append(i)

    if group != []: ret.append(group)
    return ret

def getMun(name):
    try:
        mun = Municipality.objects.get(name=name)
    except Municipality.DoesNotExist:
        mun = Municipality(name=name, mid = ID.get(name), region = getRegion(ID.get(name)))

        mun.save()
    return mun

@transaction.atomic
def saveAll(s):
    print('Saving all')
    for i in s:
        i.save()
    print('Done saving')

def getPercent():
    dic = {}
    with open(os.path.join(DPATH,PCPATH)) as f:
        for i in f:
            i = i.strip().split(',')
            dic[','.join(i[0:2])] = int(i[2])
    return dic

def addChanges():
    toSave = []
    #Add the cnages to a database
    pdic = getPercent()
    #Create a list of changes
    s = []
    with open(os.path.join(DPATH,BRPATH)) as f:
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
                try:
                    per = pdic[','.join([old,j])]
                except KeyError:
                    per = 50
                    print('Need percent for {}: {}, {}'.format(old,j,y))
                newMun = getMun(j)
                change = Changes(old=oldMun,new=newMun,percent=per,year=y)
                toSave.append(change)
        else:
            new = new[0]
            if old == new: print('{} goes into only itself'.format(old))
            newMun = getMun(new)
            change = Changes(old=oldMun,new=newMun,percent=100,year=y)
            toSave.append(change)

    saveAll(toSave)
            

def addPopulation():
    toSave = []
    #1900 to 1990, every 10 years
    with open(os.path.join(DPATH, '1901-1990.csv')) as f:
        reader = csv.reader(f, delimiter=';')
        for i in reader:
            mun = getMun(i[0])
            data = i[1:]
            for y, val in enumerate(data):
                if val == '.' or val == '-': val = 0
                try:
                    pop = Population(municipality=mun,year=1900+y*10,val=val)
                    toSave.append(pop)
                except IntegrityError:
                    print('Integrity error {}'.format(i[0]))


    #1991 to 2004 every year
    with open(os.path.join(DPATH, '1990-2004.csv')) as f:
        reader = csv.reader(f, delimiter=';')
        for i in reader:
            mun = getMun(i[0])
            data = i[1:]
            for y, val in enumerate(data):
                if val == '.' or val == '-': val = 0
                try:
                    pop = Population(municipality=mun,year=1991+y,val=val)
                    toSave.append(pop)
                except IntegrityError:
                    print('Integrity error {}'.format(i[0]))


    #2005 to 2014 every year
    with open(os.path.join(DPATH, '2004-2014.csv')) as f:
        reader = csv.reader(f, delimiter=';')
        for i in reader:
            mun = getMun(i[0])
            data = i[1:]
            for y, val in enumerate(data):
                if val == '.' or val == '-': val = 0
                try:
                    pop = Population(municipality=mun,year=2005+y,val=val)
                    toSave.append(pop)
                except IntegrityError:
                    print('Integrity error {}'.format(i[0]))

    saveAll(toSave)

def addRegions():
    global REGIONS
    with open(os.path.join(DPATH, REGIONPATH)) as f:
        reader = csv.reader(f, delimiter=',')
        for l in reader:
            REGIONS.append(Regions(name=l[0],low=int(l[1]), high=int(l[2])))    
    saveAll(REGIONS)

def addGender():
    municipalities = listMun()
    toSave = []

    classdic = {'100 ára og eldri':20}
    for i in range(20):
        classdic['{}-{} ára'.format(i*5,i*5+4)] = i
    s = []
    unknown = []
    with open(os.path.join(DPATH,GPATH)) as f:
        reader = csv.reader(f, delimiter=';')
        for i in reader:
            #There is probably a better way to do this
            if i[0] == 'Sveitarfélag' or i[1] == 'Alls': continue
            try:
                mun = Municipality.objects.get(name=i[0])
            except Municipality.DoesNotExist:
                #print('Unknown municipality {}'.format(i[0]))
                unknown.append(i[0])
                continue
    
            ageclass = classdic[i[1]]

            #should this be -1?
            for y in range(2,len(i)-1, 2):
                gpop = GenderPop(municipality=mun,ageclass=ageclass,valm=i[y],valf=i[y+1],year=1997+y//2)
                toSave.append(gpop)

    for i in set(unknown):
        print('Unknown municipality {}'.format(i))

    saveAll(toSave)

def addGroup(val,pop,name):
    global GROUPDATA
    if name in GROUPDATA:
        val = [i+j for i,j in zip(val, GROUPDATA[name][0])]
        pop += GROUPDATA[name][1]
    
    GROUPDATA[name] = (val,pop)

def addSpending():
    toSave = []
    bad, good = getGroups()
    global GROUPDATA
    #Add municipalities
    with open(os.path.join(DPATH,SPENDPATH)) as f:
        reader = csv.reader(f, delimiter=',')
        for i in reader:
            if i[0] == 'Sveitarfélag': continue
            try:
                mun = Municipality.objects.get(name=i[0])
            except Municipality.DoesnotExist:
                print('Unknown municipality {}'.format(i[0]))
                continue

            #Do I really have to do this?
            for j in range(1, len(i)): i[j] = int(i[j])

            toSave.append(SpendingPerCapita(name=i[0],income=i[1],social=i[2],health=i[3],culture=i[4],sports=i[5]))
    saveAll(toSave)


    toSave = []
    #Add grouped data, this is hella dirty
    for i in SpendingPerCapita.objects.all():
        if i.name == 'Alls': continue
        mun = Municipality.objects.get(name=i.name)
        pop = Population.objects.get(municipality=mun,year=2014).val
        val = [i.income,i.social,i.health,i.culture,i.sports]
        val = [k*pop for k in val]

        #good
        if i.name in good: addGroup(val,pop,'good')
        #bad
        if i.name in bad: addGroup(val,pop,'bad')
        #region
        reg = getRegion(mun.mid).name
        addGroup(val,pop,reg)
 

    for i in GROUPDATA:
        val,pop = GROUPDATA[i]
        i = [i] + [k//pop for k in val]

        toSave.append(SpendingPerCapita(name=i[0],income=i[1],social=i[2],health=i[3],culture=i[4],sports=i[5]))

    saveAll(toSave)


def addEdu():
    toSave = []
    with open(os.path.join(DPATH,EDUPATH)) as f:
        reader = csv.reader(f, delimiter=',')
        for i in reader:
            if i[0] == 'Landsvæði': continue
            try:
                if i[0] == 'Alls': reg = None
                else: reg = Regions.objects.get(name=i[0])
            except Regions.DoesNotExist:
                print('Unknown region {}'.format(i[0]))
                continue

            for j in range(1, len(i)):
                i[j] = int(i[j])
            edu = Education(region=reg,totalPop=i[1],childPop=i[2],grunn=i[3],framhalds=i[4],ha=i[5])
            toSave.append(edu)
    saveAll(toSave)

if __name__ == '__main__':
    import django
    django.setup()
    with open(os.path.join(DPATH, MIDPATH)) as f:
        reader = csv.reader(f, delimiter=',')
        for i in reader:
            ID[i[1]] = int(i[0])
    #Alls added here
    getMun('Alls')

    print('Adding regions')
    addRegions()
    print('Adding changes')
    addChanges()
    print('Adding population')
    addPopulation()
    print('Adding genderpop')
    addGender()
    print('Adding spending')
    addSpending()
    print('Adding education')
    addEdu()
