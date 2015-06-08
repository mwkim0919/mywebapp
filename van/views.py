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

# display all parks
def parks(request):
	# store weatherIDs
	weatherIDs = []

	# use weatherIDs as keys and store weather information in these dictionaries
	dates = {}
	wnames = {}
	d_temps = {}
	n_temps = {}
	precips = {}
	precipTypes = {}
	windSpeeds = {}
	windDirections = {}
	humidities = {}
	images = {}

	weathers = Weather.objects.order_by('date')
	# print weathers

	for weather in weathers:
		weatherIDs.append(weather.wID)
		dates[weather.wID] = weather.date
		wnames[weather.wID] = weather.name
		d_temps[weather.wID] = weather.dayTemp
		n_temps[weather.wID] = weather.nightTemp
		precips[weather.wID] = weather.precipitation
		precipTypes[weather.wID] = weather.preciType
		windSpeeds[weather.wID] = weather.windSpeed
		windDirections[weather.wID] = weather.windDirection
		humidities[weather.wID] = weather.humidity
		images[weather.wID] = "http://openweathermap.org/img/w/" + weather.image + ".png"
		# http://openweathermap.org/img/w/10d.png

	parkBox = False

	if ('parkBox' in request.GET):
		# store parkIDs in this array
		parkIDs = []

		# store park information in these dictionaries.
		# use parkID as keys
		names = {}
		streetNumbers = {}
		streetNames = {}
		facilityNumbers = {}
		facilityNames = {}
		facilities = {}
		ewStreets = {}
		nsStreets = {}
		lat = {}
		lon = {}

	    # To transfer from the database to javascript
		Parks = []
		FacilityType = []
		FacilityNum = []

	    # Sort parks alphabetically
		parks = Park.objects.order_by('pName')

	    # Construct the array and the dictionaries.
		for park in parks:
			tempFacilities = []
			Parks.append(park)
			has_facility = list(Facility.objects.filter(pID = park.pID))
			for facility in has_facility:
				f = Facility.objects.get(id = facility.id)
				fInfo = str(f.facilType) + " (" + str(f.facilNum) + ")"
				tempFacilities.append(fInfo)

		# Map park details to this park ID in the dictionaries.
			parkIDs.append(park.pID)
			names[park.pID] = park.pName
			streetNumbers[park.pID] = park.streetNumber
			streetNames[park.pID] = park.streetName
			facilities[park.pID] = tempFacilities

		# Set up the template
		template = loader.get_template('park.html')
		context = RequestContext(request, 
			{
			'parkBox': parkBox,
			'parkIDs': parkIDs,
			'names': names,
			'streetNumbers': streetNumbers,
			'streetNames': streetNames,
			'facilityNumbers': facilityNumbers,
			'facilityNames': facilityNames,
			'facilities': facilities,
			'Parks': Parks,
			'weatherIDs': weatherIDs,
			'dates': dates,
			'wnames': wnames,
			'd_temps': d_temps,
			'n_temps': n_temps,
			'precips': precips,
			'precipTypes': precipTypes,
			'windSpeeds': windSpeeds,
			'windDirections': windDirections,
			'humidities': humidities,
			'images': images,
			})

		return render(request, 'park.html', context)
	else:
		template = loader.get_template('park.html')
		context = RequestContext(request, 
		{'weatherIDs': weatherIDs,
		'dates': dates,
		'wnames': wnames,
		'd_temps': d_temps,
		'n_temps': n_temps,
		'precips': precips,
		'precipTypes': precipTypes,
		'windSpeeds': windSpeeds,
		'windDirections': windDirections,
		'humidities': humidities,
		'images': images,
		})
		return render(request, 'park.html', context)

def search(request):
	# store weatherIDs
	weatherIDs = []

	# use weatherIDs as keys and store weather information in these dictionaries
	dates = {}
	wnames = {}
	d_temps = {}
	n_temps = {}
	precips = {}
	precipTypes = {}
	windSpeeds = {}
	windDirections = {}
	humidities = {}
	images = {}

	weathers = Weather.objects.order_by('date')
	# print weathers

	for weather in weathers:
		weatherIDs.append(weather.wID)
		dates[weather.wID] = weather.date
		wnames[weather.wID] = weather.name
		d_temps[weather.wID] = weather.dayTemp
		n_temps[weather.wID] = weather.nightTemp
		precips[weather.wID] = weather.precipitation
		precipTypes[weather.wID] = weather.preciType
		windSpeeds[weather.wID] = weather.windSpeed
		windDirections[weather.wID] = weather.windDirection
		humidities[weather.wID] = weather.humidity
		images[weather.wID] = "http://openweathermap.org/img/w/" + weather.image + ".png"

	query_type = False
	query_string = False

	# query_type_ids = []
	matching_park_ids = []

	parkIDs = []

	Parks = []
	FacilityType = []
	FacilityNum = []

	names = {}
	streetNumbers = {}
	streetNames = {}
	facilityNumbers = {}
	facilityNames = {}
	facilities = {}

	if ('query_type' in request.GET):
		query_type = request.GET['query_type']
	if ('query_string' in request.GET) and request.GET['query_string'].strip():
		query_string = request.GET['query_string']

	if not query_type:
		return parks(request)

	if query_string:
		if query_type == "Park":
			similar_parks = list(Park.objects.filter(pName__icontains = query_string))
			for park in similar_parks:
				matching_park_ids.append(park.pID)

		has_parks = Park.objects.all()

		for park in has_parks:
			if (park.pID in matching_park_ids) or not query_string:
				tempFacilities = []
				Parks.append(park)
				has_facility = list(Facility.objects.filter(pID = park.pID))
				for facility in has_facility:
					f = Facility.objects.get(id = facility.id)
					fInfo = str(f.facilType) + " (" + str(f.facilNum) + ")"
					tempFacilities.append(fInfo)

				parkIDs.append(park.pID)
				names[park.pID] = park.pName
				streetNumbers[park.pID] = park.streetNumber
				streetNames[park.pID] = park.streetName
				facilities[park.pID] = tempFacilities

		if query_type == "Facility":
			similar_facilities = list(Facility.objects.filter(facilType__icontains = query_string))
			for facility in similar_facilities:
				matching_park_ids.append(facility.pID_id)

		has_parks = Park.objects.all()
		for park in has_parks:
			if (park.pID in matching_park_ids) or not query_string:
				tempFacilities = []
				Parks.append(park)
				has_facility = list(Facility.objects.filter(pID = park.pID))
				for facility in has_facility:
					f = Facility.objects.get(id = facility.id)
					fInfo = str(f.facilType) + " (" + str(f.facilNum) + ")"
					tempFacilities.append(fInfo)

				parkIDs.append(park.pID)
				names[park.pID] = park.pName
				streetNumbers[park.pID] = park.streetNumber
				streetNames[park.pID] = park.streetName
				facilities[park.pID] = tempFacilities

	# Set up the template
	template = loader.get_template('park.html')
	context = RequestContext(request, 
		{
		'query_type': query_type,
		'query_string': query_string,
		'parkIDs': parkIDs,
		'names': names,
		'streetNumbers': streetNumbers,
		'streetNames': streetNames,
		'facilities': facilities,
		'facilityNumbers': facilityNumbers,
		'facilityNames': facilityNames,
		'Parks': Parks,
		'weatherIDs': weatherIDs,
		'dates': dates,
		'wnames': wnames,
		'd_temps': d_temps,
		'n_temps': n_temps,
		'precips': precips,
		'precipTypes': precipTypes,
		'windSpeeds': windSpeeds,
		'windDirections': windDirections,
		'humidities': humidities,
		'images': images,
		})

	return render(request, 'park.html', context)

# def weathers(request):
# 	# store weatherIDs
# 	weatherIDs = []

# 	# use weatherIDs as keys and store weather information in these dictionaries
# 	dates = {}
# 	names = {}
# 	d_temps = {}
# 	n_temps = {}
# 	precips = {}
# 	precipTypes = {}
# 	windSpeeds = {}
# 	windDirections = {}
# 	humidities = {}
# 	images = {}

# 	weathers = Weather.objects.order_by('date')
# 	# print weathers

# 	for weather in weathers:
# 		weatherIDs.append(weather.wID)
# 		dates[weather.wID] = weather.date
# 		names[weather.wID] = weather.name
# 		d_temps[weather.wID] = weather.dayTemp
# 		n_temps[weather.wID] = weather.nightTemp
# 		precips[weather.wID] = weather.precipitation
# 		precipTypes[weather.wID] = weather.preciType
# 		windSpeeds[weather.wID] = weather.windSpeed
# 		windDirections[weather.wID] = weather.windDirection
# 		humidities[weather.wID] = weather.humidity
# 		images[weather.wID] = "http://openweathermap.org/img/w/" + weather.image + ".png"
# 		# http://openweathermap.org/img/w/10d.png


# 	template = loader.get_template('weather.html')
# 	context = RequestContext(request, 
# 		{
# 		'weatherIDs': weatherIDs,
# 		'dates': dates,
# 		'names': names,
# 		'd_temps': d_temps,
# 		'n_temps': n_temps,
# 		'precips': precips,
# 		'precipTypes': precipTypes,
# 		'windSpeeds': windSpeeds,
# 		'windDirections': windDirections,
# 		'humidities': humidities,
# 		'images': images,
# 		})
	
# 	return render(request, 'weather.html', context)