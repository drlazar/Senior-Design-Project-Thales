# -*- coding: utf-8 -*-
"""
Created by: Logan Mendelsohn
Edit Log:
    11/30/20 - Created the ephemeris function
"""
import tleutils as tlu
import pandas as pd
import sgp4.api as sga
import numpy as np
import matplotlib.pyplot as plt
import calculate as cd

def latlong2cart(lat, long):
    lat = np.deg2rad(lat)
    long = np.deg2rad(long)
    R_E = 6371
    x = R_E * np.cos(lat) * np.cos(long)
    y = R_E * np.cos(lat) * np.sin(long)
    z = R_E * np.sin(lat)
    
    return x, y ,z

def cart2latlong(cord):
    for i in range(len(cord)):
        
        cord[i]['r'] = np.sqrt(cord[i]['x']*cord[i]['x']+ cord[i]['y']*cord[i]['y']+ cord[i]['z']*cord[i]['z'])
        cord[i]['lat'] = np.arcsin(cord[i]['z']/cord[i]['r'])
        cord[i]['lat'] = np.degrees(cord[i]['lat'])
        cord[i]['lon'] = np.arctan2(cord[i]['y'], cord[i]['x'])
        cord[i]['lon'] = np.degrees(cord[i]['lon'])
        cord[i]['max range'] = np.arccos(6378 / cord[i]['r'])
        cord[i]['max range'] = np.degrees(cord[i]['max range'])
    return cord

# Inputs a TLE file outputs satellite coordinates in cartesian
def ephemeris(tleinput, start, end, frstart, ref):
    s, t, names = tlu.tlesplit(tleinput)
    
    satellite = []
    for i in range(len(s)):
        satellite.append(sga.Satrec.twoline2rv(s[i], t[i]))
    satarray = sga.SatrecArray(satellite)
   
    
    jdstart = start
    jdend = end
    jdinc = ref
    frarray = np.arange(frstart, frstart+1, ref)
    jdatearray = np.full(len(frarray), jdstart)
    e, r, v = satarray.sgp4(jdatearray,frarray)
    #print(frarray)
    #print(r)  # True Equator Mean Equinox position (km)
    #print(v)  # True Equator Mean Equinox velocity (km/s)
    
    index = jdatearray + frarray
    
    ephemeris = [] 
    columnnames = ["x", "y", "z"]
    for i in range(len(r)):
        
        ephemeris.append(pd.DataFrame(r[i], index, columns = columnnames))
        ephemeris[i].index.name = "Julian Date"
        
    ephemeris = cart2latlong(ephemeris)
    
    return ephemeris, names
    


def linkdist(ephemeris,stations, names):
    
    stationData = []
    for k in range(len(stations)):
        x_grd,y_grd,z_grd = latlong2cart(stations[k]["lat"], stations[k]["lon"])
        grddf = []
        grd2sat = pd.DataFrame(index = ephemeris[1].index)
        for i in range(len(ephemeris)):
            grddf.append(pd.DataFrame(index = ephemeris[i].index))
            #create columns for delta x,y,x
            grddf[i]["delta_x"] = (ephemeris[i]["x"] - x_grd)**2
            grddf[i]["delta_y"] = (ephemeris[i]["y"] - y_grd)**2
            grddf[i]["delta_z"] = (ephemeris[i]["z"] - z_grd)**2
            
            grddf[i]["In View lat"] = ephemeris[i]["max range"] > np.absolute(stations[k]["lat"] - ephemeris[i]["lat"])
            grddf[i]["In View lon"] = ephemeris[i]["max range"] > np.absolute(stations[k]["lon"] - ephemeris[i]["lon"])
            
            grddf[i]["In View"] = "False"
            
            grddf[i].loc[grddf[i]["In View lat"] & grddf[i]["In View lon"], "In View"] = "True"
            
            #calculate distance
            keytitle = names[i]
            grddf[i][keytitle] = np.sqrt(grddf[i]["delta_x"]+ grddf[i]["delta_y"] + grddf[i]["delta_z"])
            
            #grddf[i].loc[grddf[i]["In View"] == "False", keytitle] = np.NaN
            grd2sat[keytitle] = grddf[i][keytitle]
            
       
        stationData.append(grd2sat)
    stationData[0].plot()
    plt.ylabel("Distance (km)")
    plt.title("Satellite Distance vs. Julian Date")
    #print(grddf)
    #print(grd2sat)
    print(stationData)
    return stationData

def flightTest(flightData, refresh,ephemeris):
    period = refresh*86400
    flightCoord = []
    
    for i in range(len(flightData)):
        length = flightData[i]["duration"]*3600 / period
        length = int(length)
        latstep = (flightData[i]["stoplat"]-flightData[i]["startlat"])/length
        lonstep = (flightData[i]["stoplat"]-flightData[i]["startlat"])/length
        flightlat = []
        flightlon = []
        flightx = []
        flighty = []
        flightz = []
        columns = ephemeris[0].index[:length]
        for j in range(length):
            lat = flightData[i]["startlat"] + j*latstep
            lon = flightData[i]["startlon"] + j*lonstep
            x,y,z = latlong2cart(lat,lon)
            flightlat.append(lat)
            flightlon.append(lon)
            flightx.append(x)
            flighty.append(y)
            flightz.append(z)
            
        coordinates = {
            "lat": flightlat,
            "lon": flightlon,
            "x": flightx,
            "y": flighty,
            "z": flightz
            }
        temp = pd.DataFrame(coordinates,index = columns)
        flightCoord.append(temp)
    return flightCoord

def flightDist(flightCoord, ephemeris, names):
    flightDistance = []
    for i in range(len(flightCoord)):
        flightdelta = []
        flight2sat = pd.DataFrame(index = ephemeris[1].index)
        for j in range(len(ephemeris)):
            flightdelta.append(pd.DataFrame(index = ephemeris[j].index))
            #create columns for delta x,y,x
            flightdelta[j]["delta_x"] = (ephemeris[j]["x"] - flightCoord[i]["x"])**2
            flightdelta[j]["delta_y"] = (ephemeris[j]["y"] - flightCoord[i]["y"])**2
            flightdelta[j]["delta_z"] = (ephemeris[j]["z"] - flightCoord[i]["z"])**2
            
            #calculate distance
            keytitle = names[j]
            flightdelta[j][keytitle] = np.sqrt(flightdelta[j]["delta_x"]+ flightdelta[j]["delta_y"] + flightdelta[j]["delta_z"])
            flight2sat[keytitle] = flightdelta[j][keytitle]
        
        flight2sat = flight2sat[:ephemeris[0].index[len(flightCoord[i])-1]]
        flightDistance.append(flight2sat)
    return flightDistance

def minDist(data):
    minim = []
    for k in range(len(data)):
        submin = pd.DataFrame(index = data[k].index)
        submin["minDist"] = data[k].min(axis = 1)
        submin["Sat Link"] = data[k].idxmin(axis=1)
        submin.loc[submin["minDist"]== np.NaN, "Sat Link"] = "none"
        minim.append(submin)

    return minim

def linkBudget(data):
    linkData = []
    for i in range(len(data)):
        calc = cd.Calculate()
        bandwidth = 10* 10**9
        distance_km = data[i]["minDist"]
        pwr_trans_db = calc.convert_to_decibel(700)
        gain_trans_db = 35
        gain_recv_db = 20
        Tsys = 300
        MPSK = 64
        code_rate = 0.75
        overhead = 1
        rolloff = 1
        ans = calc.calc_link_budget(bandwidth, distance_km, pwr_trans_db, gain_trans_db, gain_recv_db, Tsys, MPSK, code_rate, overhead, rolloff)
        ans = pd.concat([data[i], ans], axis = 1)
        linkData.append(ans)
    
    return linkData
#Test Code
#dis = ephemeris()
#for i in range(len(dis)):
#  print(dis[i]["x"])
#eph = linkdist(dis)
#eph.plot()
#plt.ylabel("Distance (km)")
#plt.title("Satellite Distance vs. Julian Date")
