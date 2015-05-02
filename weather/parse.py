import xml.etree.ElementTree as ET
import urllib2

import datetime
from datetime import date
import sys
import time

from django.core.exceptions import ObjectDoesNotExist

from models import *

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
			name.append(sub1.find('symbol').get('name'))
			dayTemp.append(sub1.find('temperature').get('day'))
			nightTemp.append(sub1.find('temperature').get('night'))
			precipitation.append(sub1.find('precipitation').get('value'))
			preciType.append(sub1.find('precipitation').get('type'))
			windSpeed.append(sub1.find('windSpeed').get('mps'))
			windDirection.append(sub1.find('windDirection').get('name'))
			humidity.append(sub1.find('humidity').get('value'))
	
	# print date, len(date)
	# print name, len(name)
	# print dayTemp, len(dayTemp)
	# print nightTemp, len(nightTemp)
	# print precipitation, len(precipitation)
	# print preciType, len(preciType)
	# print windSpeed, len(windSpeed)
	# print windDirection, len(windDirection)
	# print humidity, len(humidity)

	for i in xrange(len(date)):
		try:
			w = Weather.objects.get(date = date[i])
		except ObjectDoesNotExist:
			if date[i] is not None:
				w = Weather(city = "Vancouver", country = "Canada", date = date[i], name = name[i],
					dayTemp = dayTemp[i], nightTemp = nightTemp[i], precipitation = precipitation[i],
					preciType = preciType[i], windSpeed = windSpeed[i], windDirection = windDirection[i],
					humidity = humidity[i])
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
			w.save()

parseWeather()
# def main():
	# parseWeather()

# if __name__ == '__main__':
	# main()