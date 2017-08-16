# -*- coding: utf-8 -*-

#!/usr/bin/env python

# NCRM8, TS673, PHYM8

#"""
#Created on Mon Sep  5 12:50:43 2016
#
#@author: tanner
#"""

import os
import subprocess32
import zipfile
import copy
import shutil
import datetime
import time
import glob
import csv

import mwWindNinja as mw

def getTime():# for diurnal winds and stability
    print "getting time..."
    masterTime=list()
    masterTime.append(str(time.time()))
    masterTime.append(str(datetime.datetime.now().year))
    masterTime.append(str(datetime.datetime.now().month))
    masterTime.append(str(datetime.datetime.now().day))
    masterTime.append(str(datetime.datetime.now().hour))
    masterTime.append(str(datetime.datetime.now().minute))
    return masterTime


def fetchReal(): #simulation weather
    print "getting weather data from MesoWest for PointInitialization"
    url=mw.stationUrlBuilder(mw.dtoken,"PHYM8",mw.var,"")
    dictData=mw.readData(url)
    mw.WriteNinjaCSV(dictData,"/home/tanner/src/wnpy2/p.csv")


def fetchWeather(): #validation weather
    print "getting weather data from MesoWest for NCRM8, TS673, PHYM8"
    url=mw.stationUrlBuilder(mw.dtoken,"NCRM8,TS673,PHYM8",mw.var,"")
    dictData=mw.readData(url)
    mw.WriteNinjaCSV(dictData,"/home/tanner/src/wnpy2/d.csv")
    
def writeKML(): #plotted kml!
    keyhole=open('/home/tanner/src/wnpy2/kml.cfg','w')
    keyhole.write('write_wx_station_kml        =   true\n')
    keyhole.write('wx_station_kml_filename     =   /home/tanner/src/wnpy2/clark.kml\n')
    keyhole.write('wx_station_filename         =   /home/tanner/src/wnpy2/d.csv\n')
    keyhole.write('elevation_file              =   /home/tanner/src/wnpy2/poph.tif\n')
    keyhole.write('initialization_method       =   pointInitialization\n')
    keyhole.write('time_zone                   =   America/Denver\n')
    keyhole.close()
    
def makeKML():
    subprocess32.call(['/home/tanner/src/build/src/cli/./WindNinja_cli','/home/tanner/src/wnpy2/kml.cfg'])
#    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wind/build/src/cli/eval/regular/regkml.cfg'])
    
    
#RUN STANDARD SIM
#RUN DIURNAL SIM
#RUN STABILITY SIM
#RUN THERMAL SIM    
    
    
    
    
fetchReal()
fetchWeather()
writeKML()
makeKML()    