#!/usr/bin/env python


# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 15:27:34 2016

@author: tanner
"""

import os
import subprocess32
import zipfile
import copy
import shutil
import datetime
import time

import sys

import mwWindNinja


def fetchKMSOWeather():
    print "getting weather data from MesoWest for PointInitialization"
    url=mwWindNinja.stationUrlBuilder(mwWindNinja.dtoken,"kmso",mwWindNinja.var,"")
    dictData=mwWindNinja.readData(url)
    mwWindNinja.WriteNinjaCSV(dictData,"/home/tanner/src/auto/point.csv")


def FetchWeather():
    print "getting weather data from MesoWest for KMSO,TR266,PNTM8"
    url=mwWindNinja.stationUrlBuilder(mwWindNinja.dtoken,"kmso,TR266,PNTM8",mwWindNinja.var,"")
    dictData=mwWindNinja.readData(url)
    mwWindNinja.WriteNinjaCSV(dictData,"/home/tanner/src/auto/data.csv")
    
    
def writeKML():
    keyhole=open('/home/tanner/src/auto/wnkml.cfg','w')
    keyhole.write('write_wx_station_kml        =   true\n')
    keyhole.write('wx_station_kml_filename     =   /home/tanner/src/auto/kmso.kml\n')
    keyhole.write('wx_station_filename         =   /home/tanner/src/auto/data.csv\n')
    keyhole.write('elevation_file              =   /home/tanner/src/auto/UV.tif\n')
    keyhole.write('initialization_method       =   pointInitialization\n')
    keyhole.write('time_zone                   =   America/Denver\n')
    keyhole.close() 
    
def makeKML():
    subprocess32.call(['/home/tanner/src/build/src/cli/./WindNinja_cli','/home/tanner/src/auto/wnkml.cfg'])
    
def writeWNcfg():
    print "writing new cfg"
    fout = open("/home/tanner/src/auto/windninja.cfg", 'w')
    fout.write('num_threads                 =   4\n') #output not written in order for wx files if >1
    #fout.write('elevation_file              =   bb_fine.tif\n')
    #fout.write('elevation_file              =   big_butte.asc\n')
    fout.write('elevation_file              =   /home/tanner/src/auto/UV.tif\n')
    fout.write('initialization_method       =   pointInitialization\n')
    fout.write('time_zone                   =   America/Denver\n')
    fout.write('output_wind_height          =   3.048\n')
    fout.write('units_output_wind_height    =   m\n')
    #fout.write('vegetation                  =   brush\n')
    fout.write('vegetation                  =   grass\n')
    fout.write('mesh_resolution             =   690\n')
    fout.write('units_mesh_resolution       =   m\n')
    fout.write('write_goog_output           =   true\n')
    fout.write('units_goog_out_resolution   =   m\n')
    fout.write('diurnal_winds               =   false\n')
    fout.write('non_neutral_stability       =   false\n')
    fout.write('wx_station_filename         =   /home/tanner/src/auto/point.csv\n')
    fout.write('write_wx_station_kml        =   true\n')
    fout.write('wx_station_kml_filename     =   /home/tanner/src/auto/other.kml\n')
    fout.write('write_ascii_output          =   true\n')
#    if(initMethod == 'pointInitialization'):
#        fout.write('wx_station_filename         =   wxstation.csv\n')
    fout.write('match_points                =   false\n')
#        fout.write('alpha_stability             =   %.2f\n' % alpha)
#    elif(initMethod == 'wxModelInitialization'):
#        fout.write('forecast_filename       =   %s\n' % wxFile)
    fout.close()
    
def runWN():
    print "Running WindNinja..."
#    subprocess32.call(['export WINDNINJA_DATA=~/src/wind/windninja/data'])
    subprocess32.call(['/home/tanner/src/build/src/cli/./WindNinja_cli','/home/tanner/src/auto/windninja.cfg'])    

fetchKMSOWeather()
FetchWeather()
writeKML()
makeKML()
writeWNcfg()
runWN()

