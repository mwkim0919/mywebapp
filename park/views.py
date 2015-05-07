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
	# store parkIDs in this array
	parkIDs = []

	# store park information in these dictionaries.
	# use parkID as keys
	names = {}
	streetNumbers = {}
	streetNames = {}
	facilityNumbers = {}
	facilityNames = {}
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
		tempFacilNames = []
		tempFacilNums = []
		Parks.append(park)
		has_facility = list(Facility.objects.filter(pID = park.pID))
		for facility in has_facility:
			f = Facility.objects.get(id = facility.id)
			tempFacilNames.append(f.facilType)
			tempFacilNums.append(f.facilNum)
		FacilityType.append(tempFacilNames)
		FacilityNum.append(tempFacilNums)

	# Map park details to this park ID in the dictionaries.
		parkIDs.append(park.pID)
		names[park.pID] = park.pName
		streetNumbers[park.pID] = park.streetNumber
		streetNames[park.pID] = park.streetName
		facilityNumbers[park.pID] = tempFacilNums
		facilityNames[park.pID] = tempFacilNames

	# print parkIDs
	# print names
	# print streetNumbers
	# print streetNames
	# print facilityNumbers
	# print facilityNames

	# Set up the template
	template = loader.get_template('home.html')
	context = RequestContext(request, 
		{'parkIDs': parkIDs,
		'names': names,
		'streetNumbers': streetNumbers,
		'streetNames': streetNames,
		'facilityNumbers': facilityNumbers,
		'facilityNames': facilityNames,
		})

	return render(request, 'home.html', context)