# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 11:31:54 2016

@author: tanner
"""

import urllib2
import json
import csv

baseurl="http://api.mesowest.net/v2/stations/latest?"
dtoken="33e3c8ee12dc499c86de1f2076a9e9d4"
var="wind_speed,wind_direction,air_temp"

def stationUrlBuilder(token,stid,svar,within):
    tokfull="&token="+token
    stidfull="stid="+stid
    svarfull="&vars="+svar
    if svar=="":
        print "downloading default variables for a WindNinja Sim"
        svarfull="&vars="+var
    timesand="&within="+str(within)
    if within=="":
        timesand=""
    network="&network=1,2"
    url=baseurl+stidfull+svarfull+network+timesand+tokfull
    return url
def radiusUrlBuilder(token,stid,radius,limit,svar,within):
    tokfull="&token="+token
    stidfull="&radius="+stid+","+radius
    svarfull="&vars="+svar
    if svar=="":
        print "downloading default variables for a WindNinja Sim"
        svarfull="&vars="+var
    timesand="&within="+str(within)
    if within=="":
        timesand=""
    limiter="&limit="+limit
    network="&network=1,2"
    url=baseurl+stidfull+svarfull+limiter+network+timesand+tokfull
    return url
    
def readData(url):
    new=urllib2.urlopen(url)
    response=new.read()
    json_string=response
    a=json.loads(json_string)
    return a
    
def WriteNinjaCSV(dictData,csvName):
    lib=dictData
    datLen=len(lib['STATION'])
    with open(csvName,'wb') as csvfile:
        blue=csv.writer(csvfile,delimiter=',')
        header=["Station_Name","Coord_Sys(PROJCS,GEOGCS)","Datum(WGS84,NAD83,NAD27)","Lat/YCoord","Lon/XCoord","Height","Height_Units(meters,feet)","Speed","Speed_Units(mph,kph,mps)","Direction(degrees)","Temperature","Temperature_Units(F,C)","Cloud_Cover(%)","Radius_of_Influence","Radius_of_Influence_Units(miles,feet,meters,km)"]
        blue.writerow(header)
        for j in range(datLen):
            obsRow=list()
            dictKey=lib['STATION'][j]['OBSERVATIONS'].keys()
            keyLen=len(dictKey)
            obsRow.append(lib['STATION'][j]['STID'])
            obsRow.append("GEOGCS")
            obsRow.append("WGS84")
            obsRow.append(lib['STATION'][j]['LATITUDE'])
            obsRow.append(lib['STATION'][j]['LONGITUDE'])
            obsRow.append("10")
            obsRow.append("meters")
            obsRow.append(lib['STATION'][j]['OBSERVATIONS']['wind_speed_value_1']['value'])
            obsRow.append("mps")
            obsRow.append(lib['STATION'][j]['OBSERVATIONS']['wind_direction_value_1']['value'])
            obsRow.append(lib['STATION'][j]['OBSERVATIONS']['air_temp_value_1']['value'])
            obsRow.append("C")
            obsRow.append("0")
            obsRow.append("-1")
            obsRow.append("km")
            blue.writerow((obsRow))
            
            
            
            
            
            
#                        obsRow.append(lib['STATION'][j]['STID']),"GEOGCS","WGS84",lib['STATION'][j]['LATITUDE'],lib['STATION'][j]['LONGITUDE'],"10","meters",lib['STATION'][j]['OBSERVATIONS']['wind_speed_value_1']['value'],"mps",lib['STATION'][j]['OBSERVATIONS']['wind_direction_value_1']['value'],lib['STATION'][j]['OBSERVATIONS']['air_temp_value_1']['value'],"C","0","-1","km")

            
            
            
            
            
            
            
            
            
            
            
            
        
