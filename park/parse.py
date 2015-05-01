import xml.etree.ElementTree as ET
import urllib2

import datetime
from datetime import date
import sys
import time

from django.core.exceptions import ObjectDoesNotExist

import park.models
from park.models import *

def parse():
	# request xml object containing information of parks in Vancouver
	url = 'ftp://webftp.vancouver.ca/opendata/xml/parks_facilities.xml'
	xml_file = urllib2.urlopen(url)
	tree = ET.ElementTree(file=xml_file)
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
		# print i
		try:
		    p = Park.objects.get(eID = i)
		except ObjectDoesNotExist:
		    if parkID[i] is not None:
		        p = Park(pID = i, pName = pName[i], streetNumber = streetNum[i], streetName = streetName[i],
		                ewStreet = ewStreet[i], nsStreet = nsStreet[i], lat = lat[i], lon = lon[i])
		        p.save()
		if parkID[i] is not None:
		    p.pName = pName[i]
		    p.streetNumber = streetNum[i]
		    p.streetName = streetName[i]
		    p.ewStreet = ewStreet[i]
		    p.nsStreet = nsStreet[i]
		    p.lat = lat[i]
		    p.lon = lon[i]
		    p.save()

	# print "ParkID: " + str(len(parkID))
	# print "name: " + str(len(name))
	# print "street#: " + str(len(streetNum))
	# print "streetName: " + str(len(streetName))
	# print "ew: " + str(len(ewStreet))
	# print "ns: " + str(len(nsStreet))
	# print "lat: " + str(len(lat)) + " lon: " + str(len(lon))
	print "ParkID" + " " + str(parkID[1])
	# print facilCount, len(facilCount)
	# print facilType, len(facilType)
	# print facilType[5][0]
	# print facilCount[5][0]

# def main():
# 	parse()

# if __name__ == '__main__':
# 	main()
