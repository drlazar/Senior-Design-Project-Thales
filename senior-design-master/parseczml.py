# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 12:22:26 2021

@author: amendelsohn_local
"""

import json 
from sgp4.api import jday

def parseczml():
    with open("tledata.czml") as f:
        czml = json.load(f)
    currentTime = czml[0]["clock"]["currentTime"]
    interval = czml[0]["clock"]["interval"]
    interval = interval.split('/')
    end = interval[1]
    return currentTime,end
#parseczml()

def utc2julian(utc):
    
    utc = utc.split('T')
    date = utc[0]
    time = utc[1]
    
    date = date.split("-")
    
    year = float(date[0])
    month = float(date[1])
    day = float(date[2])

    time = time.split(":")
    
    hour = float(time[0])
    minute = float(time[1])
    second = time[2].split("+")
    
    second = float(second[0])
    
    jd,fr = jday(year, month,day,hour,minute,second)
    
    return jd,fr
    
    
    print(time)

def grdData(inputjson):
    with open(inputjson) as f:
        data = json.load(f)
    statData = data["Station"]
    return statData

def flightData(inputjson):
    with open(inputjson) as f:
        data = json.load(f)
    flightdata = data["Flight"]
    return flightdata
