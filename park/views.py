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
			# tempFacilNames = []
			# tempFacilNums = []
			tempFacilities = []
			Parks.append(park)
			has_facility = list(Facility.objects.filter(pID = park.pID))
			for facility in has_facility:
				f = Facility.objects.get(id = facility.id)
				fInfo = str(f.facilType) + " (" + str(f.facilNum) + ")"
				tempFacilities.append(fInfo)
				# tempFacilNames.append(f.facilType)
				# tempFacilNums.append(f.facilNum)
			# FacilityType.append(tempFacilNames)
			# FacilityNum.append(tempFacilNums)

		# Map park details to this park ID in the dictionaries.
			parkIDs.append(park.pID)
			names[park.pID] = park.pName
			streetNumbers[park.pID] = park.streetNumber
			streetNames[park.pID] = park.streetName
			# facilityNumbers[park.pID] = tempFacilNums
			# facilityNames[park.pID] = tempFacilNames
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
			})

		return render(request, 'park.html', context)
	else:
		return render(request, 'park.html')

def search(request):
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
				# tempFacilNames = []
				# tempFacilNums = []
				tempFacilities = []
				Parks.append(park)
				has_facility = list(Facility.objects.filter(pID = park.pID))
				for facility in has_facility:
					f = Facility.objects.get(id = facility.id)
					fInfo = str(f.facilType) + " (" + str(f.facilNum) + ")"
					tempFacilities.append(fInfo)
					# tempFacilNames.append(f.facilType)
					# tempFacilNums.append(f.facilNum)
				# FacilityType.append(tempFacilNames)
				# FacilityNum.append(tempFacilNums)

				parkIDs.append(park.pID)
				names[park.pID] = park.pName
				streetNumbers[park.pID] = park.streetNumber
				streetNames[park.pID] = park.streetName
				facilities[park.pID] = tempFacilities
				# facilityNumbers[park.pID] = tempFacilNums
				# facilityNames[park.pID] = tempFacilNames

		if query_type == "Facility":
			similar_facilities = list(Facility.objects.filter(facilType__icontains = query_string))
			for facility in similar_facilities:
				matching_park_ids.append(facility.pID_id)

		has_parks = Park.objects.all()
		for park in has_parks:
			if (park.pID in matching_park_ids) or not query_string:
				# tempFacilNames = []
				# tempFacilNums = []
				tempFacilities = []
				Parks.append(park)
				has_facility = list(Facility.objects.filter(pID = park.pID))
				for facility in has_facility:
					f = Facility.objects.get(id = facility.id)
					fInfo = str(f.facilType) + " (" + str(f.facilNum) + ")"
					tempFacilities.append(fInfo)
					# tempFacilNames.append(f.facilType)
					# tempFacilNums.append(f.facilNum)
				# FacilityType.append(tempFacilNames)
				# FacilityNum.append(tempFacilNums)

				parkIDs.append(park.pID)
				names[park.pID] = park.pName
				streetNumbers[park.pID] = park.streetNumber
				streetNames[park.pID] = park.streetName
				facilities[park.pID] = tempFacilities
				# facilityNumbers[park.pID] = tempFacilNums
				# facilityNames[park.pID] = tempFacilNames

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
		})

	return render(request, 'park.html', context)