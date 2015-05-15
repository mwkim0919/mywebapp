# Create your models here.
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator

#-------------------------------------------------------------------------------
# Main entity sets.
#-------------------------------------------------------------------------------

class Weather(models.Model):
	PRECI_TYPES = (
        ('rain', 'rain'),
        ('snow', 'snow'),
	)
	wID = models.AutoField('Weather ID', primary_key = True)
	city = models.CharField('City', max_length = 20, null = True, blank = True)
	country = models.CharField('Country', max_length = 20, null = True, blank = True)
	date = models.DateField()
	name = models.CharField('Name', max_length = 20, null = True, blank = True)
	dayTemp = models.FloatField('Day Temperature', max_length = 10, null = True, blank = True)
	nightTemp = models.FloatField('Night Temperature', max_length = 10, null = True, blank = True)
	precipitation = models.FloatField('Precipitation', max_length = 10, null = True, blank = True)
	preciType = models.CharField('Precipitation Type', choices = PRECI_TYPES, max_length = 10, null = True, blank = True)
	windSpeed = models.FloatField('Wind Speed', max_length = 10, null = True, blank = True)
	windDirection = models.CharField('Wind Direction', max_length = 20, null = True, blank = True)
	humidity = models.IntegerField('Humidity', validators = [MinValueValidator(0), MaxValueValidator(100)], 
		null = True, blank = True)
	image = models.CharField('Image', max_length = 5, null = True, blank = True)

	class Meta:
	    ordering = ['date']

	def __unicode__(self):
	    return unicode(self.date)
