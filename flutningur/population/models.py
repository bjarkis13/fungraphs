from django.db import models

class Regions(models.Model):
    name = models.CharField(max_length=200, unique=True)
    low = models.IntegerField(unique=True, null=False)
    high = models.IntegerField(unique=True, null=False)

class Municipality(models.Model): 
    name = models.CharField(max_length=200, unique=True)
    mid = models.IntegerField(unique=True, null=True)
    change = models.ManyToManyField('self', symmetrical=False, through='Changes', through_fields=('old','new'))
    region = models.ForeignKey(Regions, null=True)

class Changes(models.Model):
    old = models.ForeignKey(Municipality, related_name='municipality_old')
    new = models.ForeignKey(Municipality, related_name='municipality_new')
    percent = models.FloatField()
    year = models.IntegerField()

class Population(models.Model):
    municipality = models.ForeignKey(Municipality)
    year = models.IntegerField()
    val = models.IntegerField(null=True)

    class Meta:
        unique_together = ('municipality', 'year')

class GenderPop(models.Model):
    municipality = models.ForeignKey(Municipality)	
    ageclass = models.IntegerField() #0 for 0-4, 1 for 5-9 etc.
    valm = models.IntegerField()
    valf = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        unique_together = ('municipality', 'year', 'ageclass')

class SpendingPerCapita(models.Model):
	municipality = models.ForeignKey(Municipality)
	taxIncome = models.IntegerField()
	social = models.IntegerField()
	health = models.IntegerField()
	culture = models.IntegerField()
	sports = models.IntegerField()
	year = models.IntegerField()

#Data from 2012
class Education(models.Model):
	region = models.OneToOneField(Regions,null=True)
	totalPop = models.IntegerField()
	childPop = models.IntegerField()
	grunn = models.IntegerField()
	framhalds = models.IntegerField()
	ha = models.IntegerField()
