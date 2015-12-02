from django.db import models

# Create your models here.
class Municipality(models.Model): 
    name = models.CharField(max_length=200, unique=True)
    change = models.ManyToManyField('self', symmetrical=False, through='Changes', through_fields=('old','new'))

class Changes(models.Model):
    old = models.ForeignKey(Municipality, related_name='municipality_old')
    new = models.ForeignKey(Municipality, related_name='municipality_new')
    percent = models.FloatField()
    year = models.IntegerField()

class Population(models.Model):
    municipality = models.ForeignKey(Municipality)
    year = models.IntegerField()
    val = models.IntegerField(null=True)
