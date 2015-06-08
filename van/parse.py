import xml.etree.ElementTree as ET
import urllib2

import json

import datetime
from datetime import date
import sys
import time

from django.core.exceptions import ObjectDoesNotExist

from models import *

def parsePark():
	# request xml object containing information of parks in Vancouver
	url = 'ftp://webftp.vancouver.ca/opendata/xml/parks_facilities.xml'
	xml_file = urllib2.urlopen(url)
	tree = ET.ElementTree(file = xml_file)
	root = tree.getroot()

	# initialize arrays to store the data from xml file
	parkID = []
	name = []
	streetNum = []
	streetName = []
	ewStreet = []
	nsStreet = []
	lat = []
	lon = []
	facil = []
	facilCount = []
	facilType = []
	# washroom = []
	
	# add park information into the arrays
	for child in root.iter('Park'):
		parkID.append(child.attrib)
		name.append(child.find('Name').text)
		streetNum.append(child.find('StreetNumber').text)
		streetName.append(child.find('StreetName').text)
		ewStreet.append(child.find('EWStreet').text)
		nsStreet.append(child.find('NSStreet').text)
		latlon = child.find('GoogleMapDest').text
		array = latlon.split(',')
		lat.append(array[0])
		lon.append(array[1])

	# add facility information into arrays
	for child in root.iter('Park'):
		for sub1 in child.iter('Facilities'):
			temp = []
			temp2 = []
			for sub2 in sub1.iter('Facility'):
				temp.append(sub2.find('FacilityCount').text)
				temp2.append(sub2.find('FacilityType').text)
			facilCount.append(temp)
			facilType.append(temp2)

	for i in xrange(len(parkID)):
		try:
		    p = Park.objects.get(pID = i+1)
		except ObjectDoesNotExist:
		    if parkID[i] is not None:
		        p = Park(pName = name[i], streetNumber = streetNum[i], streetName = streetName[i],
		                ewStreet = ewStreet[i], nsStreet = nsStreet[i], lat = lat[i], lon = lon[i])
		        p.save()
		if parkID[i] is not None:
		    p.pName = name[i]
		    p.streetNumber = streetNum[i]
		    p.streetName = streetName[i]
		    p.ewStreet = ewStreet[i]
		    p.nsStreet = nsStreet[i]
		    p.lat = lat[i]
		    p.lon = lon[i]
		    p.save()

	for i in xrange(len(parkID)):
		for j in xrange(len(facilCount[i])):
			try:
				f = Facility.objects.get(pID = Park.objects.get(pID = i+1), facilType = facilType[i][j])
			except ObjectDoesNotExist:
				if parkID[i] and facilCount[i][j] is not None:
					f = Facility(pID = Park.objects.get(pID = i+1), facilNum = facilCount[i][j], facilType = facilType[i][j])
					f.save()
			if parkID[i] and facilCount[i][j] is not None:
				f.pID = Park.objects.get(pID = i+1)
				f.facilNum = facilCount[i][j]
				f.facilType = facilType[i][j]
				f.save()

	lu = Last_Updated.objects.order_by('-updateCount')[0]
	lu.date = datetime.date.today()
	lu.updateCount = lu.updateCount + 1
	lu.save()

# Update the database if it hasn't been updated yet.
if len(Last_Updated.objects.order_by('-updateCount')) == 0:
	lu = Last_Updated(date = datetime.date.today(), updateCount = 1)
	lu.save()

# Update the database everyday.
currDate = datetime.date.today()
lastUpdate = Last_Updated.objects.order_by('-updateCount')[0]
lastUpdate = str(lastUpdate)
lastUpdate = lastUpdate.replace('-', ' ')
lastUpdate = lastUpdate.split(' ')
lastUpdate = [int(x) for x in lastUpdate]
lastDate = datetime.date(lastUpdate[0], lastUpdate[1], lastUpdate[2])
diff = currDate - lastDate

# print "work!!!"
# print Park.objects.all().count()
if (diff.days >= 100 or Park.objects.all().count() == 0):
	parsePark()



def parseWeather():
	# request xml object containing information of weather in Vancouver
	APIKEY = "233266d17f328a2830af73910929e676"
	URL = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Vancouver&mode=xml&units=metric&cnt=7&APPID=" + APIKEY
	xml_file = urllib2.urlopen(URL)
	tree = ET.ElementTree(file = xml_file)
	root = tree.getroot()
	# print root

	# initialize arrays to store the data from xml file
	# city = []
	image = []
	date = []
	name = []
	dayTemp = []
	nightTemp = []
	precipitation = []
	preciType = []
	windSpeed = []
	windDirection = []
	humidity = []

	# add weather info into the arrays
	for child in root.iter('forecast'):
		for sub1 in child.findall('time'):
			date.append(sub1.get('day'))
			image.append(sub1.find('symbol').get('var'))
			name.append(sub1.find('symbol').get('name'))
			dayTemp.append(sub1.find('temperature').get('day'))
			nightTemp.append(sub1.find('temperature').get('night'))
			precipitation.append(sub1.find('precipitation').get('value'))
			preciType.append(sub1.find('precipitation').get('type'))
			windSpeed.append(sub1.find('windSpeed').get('mps'))
			windDirection.append(sub1.find('windDirection').get('name'))
			humidity.append(sub1.find('humidity').get('value'))

	Weather.objects.all().delete()

	for i in xrange(len(date)):
		try:
			w = Weather.objects.get(date = date[i])
		except ObjectDoesNotExist:
			if date[i] is not None:
				w = Weather(city = "Vancouver", country = "Canada", date = date[i], name = name[i],
					dayTemp = dayTemp[i], nightTemp = nightTemp[i], precipitation = precipitation[i],
					preciType = preciType[i], windSpeed = windSpeed[i], windDirection = windDirection[i],
					humidity = humidity[i], image = image[i])
				w.save()
		if date[i] is not None:
			w.city = "Vancouver"
			w.country = "Canada"
			w.date = date[i]
			w.name = name[i]
			w.dayTemp = dayTemp[i]
			w.nightTemp = nightTemp[i]
			w.precipitation = precipitation[i]
			w.preciType = preciType[i]
			w.windSpeed = windSpeed[i]
			w.windDirection = windDirection[i]
			w.humidity = humidity[i]
			w.image = image[i]
			w.save()

parseWeather()