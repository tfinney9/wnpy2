# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 09:38:32 2016

@author: tanner
"""

import os
import subprocess32
import zipfile
import copy
import shutil
import git
import datetime
import time
import glob
import csv

import mwWindNinja as mw

def fetchReal():
    print "getting weather data from MesoWest for PointInitialization"
    url=mw.stationUrlBuilder(mw.dtoken,"PHYM8",mw.var,"")
    dictData=mw.readData(url)
    mw.WriteNinjaCSV(dictData,"/home/tanner/src/wind/build/src/cli/eval/regular/stableP.csv")


def fetchWeather():
    print "getting weather data from MesoWest for NCRM8, TS673, PHYM8"
    url=mw.stationUrlBuilder(mw.dtoken,"NCRM8,TS673,PHYM8",mw.var,"")
    dictData=mw.readData(url)
    mw.WriteNinjaCSV(dictData,"/home/tanner/src/wind/build/src/cli/eval/regular/stableD.csv")
def writeKML():
    keyhole=open('/home/tanner/src/wind/build/src/cli/eval/regular/regkml.cfg','w')
    keyhole.write('write_wx_station_kml        =   true\n')
    keyhole.write('wx_station_kml_filename     =   /home/tanner/src/wind/build/src/cli/eval/regular/stableClark.kml\n')
    keyhole.write('wx_station_filename         =   /home/tanner/src/wind/build/src/cli/eval/regular/stableD.csv\n')
    keyhole.write('elevation_file              =   /home/tanner/src/wind/build/src/cli/eval/poph.tif\n')
    keyhole.write('initialization_method       =   pointInitialization\n')
    keyhole.write('time_zone                   =   America/Denver\n')
    keyhole.close() 
    
def writeWNcfg():
    print "writing new cfg"
    fout = open("/home/tanner/src/wind/build/src/cli/eval/regular/reg.cfg", 'w')
    fout.write('num_threads                 =   4\n') #output not written in order for wx files if >1
    #fout.write('elevation_file              =   bb_fine.tif\n')
    #fout.write('elevation_file              =   big_butte.asc\n')
    fout.write('elevation_file              =   /home/tanner/src/wind/build/src/cli/eval/poph.tif\n')
    fout.write('initialization_method       =   pointInitialization\n')
    fout.write('time_zone                   =   America/Denver\n')
    fout.write('output_wind_height          =   3.048\n')
    fout.write('units_output_wind_height    =   m\n')
    fout.write('vegetation                  =   trees\n')
#    fout.write('vegetation                  =   grass\n')
    fout.write('mesh_resolution             =   690\n')
    fout.write('units_mesh_resolution       =   m\n')
    fout.write('write_goog_output           =   true\n')
    fout.write('units_goog_out_resolution   =   m\n')
    fout.write('diurnal_winds               =   false\n')
    fout.write('non_neutral_stability       =   false\n')
    fout.write('wx_station_filename         =   /home/tanner/src/wind/build/src/cli/eval/regular/stableP.csv\n')
    fout.write('write_wx_station_kml        =   true\n')
    fout.write('wx_station_kml_filename     =   /home/tanner/src/wind/build/src/cli/eval/regular/stableOther.kml\n')
    fout.write('write_ascii_output          =   true\n')
    fout.write('output_path                 =   /home/tanner/src/wind/build/src/cli/eval/regular')
#    if(initMethod == 'pointInitialization'):
#        fout.write('wx_station_filename         =   wxstation.csv\n')
#        fout.write('match_points                =   false\n')
#        fout.write('alpha_stability             =   %.2f\n' % alpha)
#    elif(initMethod == 'wxModelInitialization'):
#        fout.write('forecast_filename       =   %s\n' % wxFile)
    fout.close()
    
def makeKML():
    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wind/build/src/cli/eval/regular/regkml.cfg'])
def runWN():
    print "Running WindNinja...Neutral Stability, no Diurnal Winds!!!!"
#    subprocess32.call(['export WINDNINJA_DATA=~/src/wind/windninja/data'])
    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wind/build/src/cli/eval/regular/reg.cfg'])

def renameFile():
    print "renaming Files"
    os.rename('/home/tanner/src/wind/build/src/cli/eval/regular/poph_point_690m.kmz','/home/tanner/src/wind/build/src/cli/eval/regular/pRG.zip')
    os.rename('/home/tanner/src/wind/build/src/cli/eval/regular/poph_point_690m_vel.asc','/home/tanner/src/wind/build/src/cli/eval/regular/velRG.asc')
    os.rename('/home/tanner/src/wind/build/src/cli/eval/regular/poph_point_690m_ang.asc','/home/tanner/src/wind/build/src/cli/eval/regular/angRG.asc')
def extractZIP():
    print "extracting KMLs from ZIP"
    with zipfile.ZipFile('/home/tanner/src/wind/build/src/cli/eval/regular/pRG.zip',"r") as z:
        z.extractall('/home/tanner/src/wind/build/src/cli/eval/regular')
def renameZIPExtracts():
    print "renaming zip extracts"
    os.rename('/home/tanner/src/wind/build/src/cli/eval/regular/poph_point_690m.kml','/home/tanner/src/wind/build/src/cli/eval/regular/pRG.kml')
    os.rename('/home/tanner/src/wind/build/src/cli/eval/regular/poph_point_690m.bmp','/home/tanner/src/wind/build/src/cli/eval/regular/pRG.bmp') 
     
def writeVelocityData():
    info=time.time()
    m=list(csv.reader(open('/home/tanner/src/wind/build/src/cli/eval/regular/stableD.csv','rb')))
    vel=list(csv.reader(open('/home/tanner/src/wind/build/src/cli/eval/regular/velRG.asc','rb'),delimiter='\t'))
    
    nnNCRM8=vel[41][14]
    nnTS673=vel[14][6]
    nnPHYM8=vel[24][28]
    PHYM8=m[1][7]
    TS673=m[2][7]
    NCRM8=m[3][7]
    
    
    with open('/home/tanner/src/wind/build/src/cli/eval/regular/rgVelocityVal.csv','a') as csvfile:
        blue=csv.writer(csvfile,delimiter=',')
        dat=[info,NCRM8,nnNCRM8,TS673,nnTS673,PHYM8,nnPHYM8]
        blue.writerow(dat)
        
def writeAngleData():
    info=time.time()
    m=list(csv.reader(open('/home/tanner/src/wind/build/src/cli/eval/regular/stableD.csv','rb')))
    vel=list(csv.reader(open('/home/tanner/src/wind/build/src/cli/eval/regular/angRG.asc','rb'),delimiter='\t'))
    
    nnNCRM8=vel[41][14]
    nnTS673=vel[14][6]
    nnPHYM8=vel[24][28]
    PHYM8=m[1][7]
    TS673=m[2][7]
    NCRM8=m[3][7]
    
    
    with open('/home/tanner/src/wind/build/src/cli/eval/regular/rgAngleVal.csv','a') as csvfile:
        blue=csv.writer(csvfile,delimiter=',')
        dat=[info,NCRM8,nnNCRM8,TS673,nnTS673,PHYM8,nnPHYM8]
        blue.writerow(dat)        
        
        
        
        
        