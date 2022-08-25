
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 13:44:50 2020

@author: amendelsohn_local
"""
from tletools import TLE
import json
import urllib.request as ur
from satellite_czml import satellite_czml


# Pulls a TLE text file from a URL saves it to a local file   
def tleupdate():
    
    txt = ur.urlopen("https://www.celestrak.com/NORAD/elements/x-comm.txt").read()
    f = open("experimental.txt", "wb")
    f.write(txt)
    print(txt)

# splits TLE into desired format for sgp4
def tlesplit(tlefile):
    
    satnames = []
    line1 = []
    line2 = []
    
    f = open(tlefile, "r")
    
    tledata = f.read().splitlines()
    
    for i in range(len(tledata)):
        if (tledata[i][0] == '1'):
            line1.append(tledata[i])
        elif (tledata[i][0] == '2'):
            line2.append(tledata[i])
        else:
            satnames.append(tledata[i])
    
    print(satnames)
    return line1, line2, satnames

# Writes a czml file from TLE            
def tle2czml(tleinput):
    line1, line2, satnames = tlesplit(tleinput)
    #single_tle = [['ISS (ZARYA)',
    #           '1 25544U 98067A   21016.23305200  .00001366  00000-0  32598-4 0  9992',
    #           '2 25544  51.6457  14.3113 0000235 231.0982 239.8264 15.49297436265049']]
    
    multiple_tle = []
    for i in range(len(satnames)):
        temp_tle = []
        temp_tle.append(satnames[i])
        temp_tle.append(line1[i])
        temp_tle.append(line2[i])
        multiple_tle.append(temp_tle)
    #print(multiple_tle)
    czml_string = satellite_czml(tle_list=multiple_tle).get_czml()
    #print(czml_string)
    
    f = open("tledata.czml", "w")
    f.write(czml_string)

# Converts TLE to a JSON format
def tle2json(tlein, jsonout):
    
    tledict = {}
    tledict['Satellite'] = []
    tle1 = TLE.load(tlein)
    
    for i in range(len(tle1)):
        tledict['Satellite'].append(tle1[i].asdict())
        
        
    with open(jsonout, 'w') as outjson:
        json.dump(tledict, outjson, indent = 4)
        
# tle2json("tledata.txt", "json1.json")

# Merges 2 tle json files
def mergejson(tlejson, jsonin, jsonout = 0):
    with open(jsonin) as f:
        linkdata = json.load(f)
    with open(tlejson) as g:
        tledata = json.load(g)
    
    for i in range(len(tledata["Satellite"])):
        linkdata["Satellite"].append(tledata["Satellite"][i])
        
    if jsonout != 0:
        with open(jsonout, 'w') as jout:
            json.dump(linkdata, jout, indent = 4)
    else:
        with open(jsonin, 'w') as jin:
            json.dump(linkdata, jin, indent = 4)
        
# mergejson("json1.json", "testJSON.json")

# converts a json file to TLE
def json2tle(jsonin, tleout):
    
    # Open the JSON file and read it into a list
    with open(jsonin) as f:
        linkdata = json.load(f)
    satdata = linkdata["Satellite"]
    
    #initialize the strings to carry the TLE
    tlestrings = []
    
    #loop through each element in 
    for i in range(len(satdata)):
        #save the data into a local variable
        name = satdata[i]["name"]
        norad = satdata[i]["norad"]
        classification = satdata[i]["classification"]
        int_desig = satdata[i]["int_desig"]
        epoch_year = satdata[i]["epoch_year"]
        epoch_day = satdata[i]["epoch_day"]
        dn_o2 = satdata[i]["dn_o2"]
        ddn_o6 = satdata[i]["ddn_o6"]
        bstar = satdata[i]["bstar"]
        set_num = satdata[i]["set_num"]
        inc = satdata[i]["inc"]
        raan = satdata[i]["raan"]
        ecc = satdata[i]["ecc"]
        argp = satdata[i]["argp"]
        M = satdata[i]["M"]
        n = satdata[i]["n"]
        rev_num = satdata[i]["rev_num"]
        
        #Convert certain values into strings
        str_epoch_year = str(epoch_year)[2:4]
        str_epoch_day = str('{:<012}'.format(epoch_day))
        if dn_o2 < 0:
            tempstr = str('{:<011f}'.format(dn_o2))
            str_dn_o2 = "-" + tempstr[1:].lstrip("0")
        else:
            str_dn_o2 = " " + str('{:<010f}'.format(dn_o2)).lstrip("0")
        #MAY have to modify later
        if ddn_o6 < 0:
            tempstr = str('{:.5e}'.format(ddn_o6))
            str_ddn_o6 = "-" + tempstr[3:8] + tempstr[9] + tempstr[11]
        else:
            tempstr = str('{:.5e}'.format(ddn_o6))
            str_ddn_o6 = " " + tempstr[2:7] + tempstr[8] + tempstr[10]
        if bstar < 0:
            tempstr = str('{:.5e}'.format(bstar))
            str_bstar = "-" + tempstr[1] + tempstr[3:7] + tempstr[9] + (str(int(tempstr[11])-1))
        else:
            tempstr = str('{:.5e}'.format(bstar))
            str_bstar = " " + tempstr[2] + tempstr[2:6] + tempstr[8] 
            if int(tempstr[10]) > 0:
                str_bstar = str_bstar + (str(int(tempstr[10])-1))
            else:
                str_bstar = str_bstar + "0"
        if (set_num < 0):
            str_set_num = str(set_num)
        else: 
            str_set_num = " " + str(set_num)
        
        #strings for line 2
        str_inc = str(inc)
        str_raan = str(raan)
        str_ecc = str(ecc)
        str_argp = str(argp)
        str_M = str(M)
        str_n = str(n)
        str_rev_num = str(rev_num)
        
        #add checksum later
        #temptle = TLE(name,norad,classification,int_desig,epoch_year, epoch_day,
                      #dn_o2, ddn_o6, bstar, set_num, inc, raan, ecc, argp, M, n, rev_num)
        #Create the TLE line 1
        string1 = "1" + ' ' + norad + classification +  ' ' + int_desig
        string1 = string1 + " " + str_epoch_year + str_epoch_day
        string1 = string1 + " " + str_dn_o2 + " " + str_ddn_o6
        string1 = string1 + " " + str_bstar + " 0 " + str_set_num + "0"
        print(string1)
        
        string2 = "2 " + norad + " " + str_inc + " " + str_raan
        string2 = string2 + " " + str_ecc + " " + str_argp + " " + str_M
        string2 = string2 + " " + str_n + " " + str_rev_num
        print(string2)
        
        #create the TLEstring
        tempTLE = name + "\n" + string1 + "\n" + string2 + "\n"
        with open(tleout, 'a') as tl:
            tl.write(tempTLE)
            
        #clear string 1 for next loop
        string1 = ""
        string2 = ""
        
#json2tle("testJSON.json","functioncheck.txt")
#tlesplit("iridium.txt")
tleupdate()
#tle2czml()