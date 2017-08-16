#!/usr/bin/env python

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
import plot2

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
    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wnpy2/kml.cfg'])
#    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wind/build/src/cli/eval/regular/regkml.cfg'])
    
def writeLogFile(ini):
    print "writing logFile..."
    runtime=str(datetime.datetime.now().time())
    unix=str(time.time())
    log=open('/home/tanner/ninjaoutput/thermal/thermalLog.txt','w')
    log.write("Last Updated At: ")
    log.write(runtime)
    log.write("| UnixTime: ")
    log.write(unix)
    log.write("\n")
    log.write("Simulation Type: PointInitialization, Diurnal Winds, Non-Neutral Stability, 690m\n")
    final=time.time()
    dur=final-ini
    log.write("Runtime: ")
    log.write(str(dur))
    
start=time.time()    
fetchReal()
fetchWeather()
writeKML()
makeKML()       
    
#RUN STANDARD SIM
import standard2
standard2.RunStandard2()
##RUN DIURNAL SIM
import diurnal2
diurnal2.runDiurnal2()
#RUN STABILITY SIM
import stability2
stability2.runStability2()
#RUN THERMAL SIM    
import thermal2
thermal2.runThermal2()

#MAKE PLOTS
stepdata=plot2.CreateSteps()
stationData=plot2.AssembleData()
plot2.plotVelocity("/home/tanner/ninjaoutput/thermal/NCRM8.png","NCRM8",0,2,"A",stationData,stepdata)
plot2.plotVelocity("/home/tanner/ninjaoutput/thermal/TS673.png","TS673",1,2,"A",stationData,stepdata)
plot2.plotVelocity("/home/tanner/ninjaoutput/thermal/PHYM8.png","PHYM8",2,2,"A",stationData,stepdata)

#WRITE LOG FILE
writeLogFile(start)

#MOVE META FILES
shutil.copyfile('/home/tanner/src/wnpy2/clark.kml','/home/tanner/ninjaoutput/thermal/clark.kml')
#metafiles: logfile, plots, clark.kml
    
    
    
    
 