# Create your views here.
import datetime
import urllib2

from django.contrib import auth
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from django.utils import timezone

# from forms import RegistrationForm
from models import *
from parse import *

def weathers(request):

	# store weatherIDs
	weatherIDs = []

	# use weatherIDs as keys and store weather information in these dictionaries
	dates = {}
	names = {}
	d_temps = {}
	n_temps = {}
	precips = {}
	precipTypes = {}
	windSpeeds = {}
	windDirections = {}
	humidities = {}

	weathers = Weather.objects.order_by('date')
	print weathers

	for weather in weathers:
		weatherIDs.append(weather.wID)
		dates[weather.wID] = weather.date
		names[weather.wID] = weather.name
		d_temps[weather.wID] = weather.dayTemp
		n_temps[weather.wID] = weather.nightTemp
		precips[weather.wID] = weather.precipitation
		precipTypes[weather.wID] = weather.preciType
		windSpeeds[weather.wID] = weather.windSpeed
		windDirections[weather.wID] = weather.windDirection
		humidities[weather.wID] = weather.humidity

	template = loader.get_template('weather.html')
	context = RequestContext(request, 
		{'weatherIDs': weatherIDs,
		'dates': dates,
		'names': names,
		'd_temps': d_temps,
		'n_temps': n_temps,
		'precips': precips,
		'precipTypes': precipTypes,
		'windSpeeds': windSpeeds,
		'windDirections': windDirections,
		'humidities': humidities,
		})
	
	return render(request, 'weather.html', context)