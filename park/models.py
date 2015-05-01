# Create your models here.
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

#-------------------------------------------------------------------------------
# Main entity sets.
#-------------------------------------------------------------------------------

class Park(models.Model):
    pID = models.AutoField('Park ID', primary_key = True)
    pName = models.CharField('Park Name', max_length = 50, null = True, blank = True)
    streetNumber = models.IntegerField('Street #', max_length = 10, null = True, blank = True)
    streetName = models.CharField('Street Name', max_length = 50, null = True, blank = True)
    ewStreet = models.CharField('ewStreet', max_length = 50, null = True, blank = True)
    nsStreet = models.CharField('nsStreet', max_length = 50, null = True, blank = True)
    lat = models.FloatField('Latitude', null = True, blank = True)
    lon = models.FloatField('Longitude', null = True, blank = True)

    class Meta:
        ordering = ['pID']
    
    def __unicode__(self):
        return self.pName

class Facility(models.Model):

	pID = models.ForeignKey(Park, verbose_name = u'Park ID')
	facilNum = models.IntegerField('Facility #', max_length = 3, null = True, blank = True)
	facilType = models.CharField('Facility Type', max_length = 50, null = True, blank = True)

	class Meta:
		ordering = ['pID']
		verbose_name_plural = 'Facility'

	def __unicode__(self):
		return str(self.pID_id) + " - " + self.facilType

#-------------------------------------------------------------------------------
# Keeps track of when the database was last updated.
#-------------------------------------------------------------------------------

class Last_Updated(models.Model):
    date = models.DateField()
    updateCount = models.IntegerField('Update count')
    
    class Meta:
        verbose_name_plural = 'Last_Updated'

    def __unicode__(self):
        return u'%s' % self.date
