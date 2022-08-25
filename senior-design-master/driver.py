# -*- coding: utf-8 -*-
"""
created by: Logan Mendelsohn
updated: 3/2/2021
"""
import tleutils as tleu
import ephemeris as eph
import parseczml as pc
import writeczml as wc
import linkplot as lp
import matplotlib.pyplot as plt


tlefile = "tledata.txt"
inputjson = "input.json"

#refresh rate
refresh = 0.02

# update tle files with url if necessary
# tleu.tleupdate()

#download groundstation data
stations = pc.grdData(inputjson)

#download flightdata
flight = pc.flightData(inputjson)

#create czml code for orbit graphics
tleu.tle2czml(tlefile)

#Find start and end time of czml
start,end = pc.parseczml()

#Convert UTC to julian date
jdstart,frstart = pc.utc2julian(start)
jdend,frend = pc.utc2julian(end)

#generate ephemeris of satellites
ephemeris, names = eph.ephemeris(tlefile, jdstart,jdend, frstart, refresh)


#generate flight coordinates
flightCoord = eph.flightTest(flight, refresh,ephemeris)

#generate data for flight
flightdist = eph.flightDist(flightCoord, ephemeris, names)
flightData = eph.minDist(flightdist)
flightLink = eph.linkBudget(flightData)

#generate data for each ground station
grddata = eph.linkdist(ephemeris,stations, names)
datalength = len(grddata[0])

#find minimum values for grdstation
data = eph.minDist(grddata)

#find linkData
linkData = eph.linkBudget(data)

#find czml descriptions
descriptions = wc.grddescriptions(linkData)

#find flight descriptions
flightdesc = wc.grddescriptions(flightLink)


#find interval boundaries
bound = wc.timeBound(start, end, refresh, datalength)

#create intervals from boundaries
intervals = wc.interval(bound)

#generate entrues for czml file
desEntry = wc.descriptionEntry(descriptions, intervals)

#generate descriptions for flight czml
flightdesc = wc.grddescriptions(flightLink)

#generate entry for flight
flightEntry = wc.descriptionEntry(flightdesc, intervals)

#generate coordinates in czml format
cart = wc.cartesian4(flightCoord, refresh)

#find availability of flight
availability = wc.availability(bound, flightCoord)

wc.grdczml(desEntry, stations, flightEntry, cart, start, availability, end)

#plot some functions in python



