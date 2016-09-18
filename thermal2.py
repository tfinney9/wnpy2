# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 12:51:58 2016

@author: tanner

THERMAL PARAMATERIZATIONS ON (DIURNAL WINDS AND NON-NEUTRAL STABILITY)
"""
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

def getTime():
    masterTime=list()
    masterTime.append(str(time.time()))
    masterTime.append(str(datetime.datetime.now().year))
    masterTime.append(str(datetime.datetime.now().month))
    masterTime.append(str(datetime.datetime.now().day))
    masterTime.append(str(datetime.datetime.now().hour))
    masterTime.append(str(datetime.datetime.now().minute))
    return masterTime

def writeWNcfg(m):
    print "writing new cfg"
    fout = open("/home/tanner/src/wnpy2/thermal/thermal.cfg", 'w')
    fout.write('num_threads                 =   4\n') #output not written in order for wx files if >1
    #fout.write('elevation_file              =   bb_fine.tif\n')
    #fout.write('elevation_file              =   big_butte.asc\n')
    fout.write('elevation_file              =   /home/tanner/src/wnpy2/poph.tif\n')
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
    fout.write('diurnal_winds               =   true\n')
    fout.write('year                        =   %s\n' % m[1])
    fout.write('month                       =   %s\n' % m[2])
    fout.write('day                         =   %s\n' % m[3])
    fout.write('hour                        =   %s\n' % m[4])
    fout.write('minute                      =   %s\n' % m[5])
    fout.write('non_neutral_stability       =   true\n')
    fout.write('wx_station_filename         =   /home/tanner/src/wnpy2/p.csv\n')
    fout.write('write_wx_station_kml        =   false\n')
    fout.write('wx_station_kml_filename     =   /home/tanner/src/wnpy2/thermal/backup.kml\n')
    fout.write('write_ascii_output          =   true\n')
    fout.write('output_path                 =   /home/tanner/src/wnpy2/thermal/\n')
#    if(initMethod == 'pointInitialization'):
#        fout.write('wx_station_filename         =   wxstation.csv\n')
    fout.write('match_points                =   false\n')
#        fout.write('alpha_stability             =   %.2f\n' % alpha)
#    elif(initMethod == 'wxModelInitialization'):
#        fout.write('forecast_filename       =   %s\n' % wxFile)
    fout.close()
    
def runWN():
    print "Running WindNinja... thermal.py"
#    subprocess32.call(['export WINDNINJA_DATA=~/src/wind/windninja/data'])
    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wnpy2/thermal/thermal.cfg'])
#    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wind/build/src/cli/eval/regular/reg.cfg'])
        
def renameFiles():
    print "renaming files..."
    kmz=glob.glob('/home/tanner/src/wnpy2/thermal/*.kmz')
    os.rename(kmz[0],'/home/tanner/src/wnpy2/thermal/pThermal.zip')
    vel=glob.glob('/home/tanner/src/wnpy2/thermal/*_vel.asc')
    ang=glob.glob('/home/tanner/src/wnpy2/thermal/*_ang.asc')
    os.rename(vel[0],'/home/tanner/src/wnpy2/thermal/data/velThermal.asc')
    os.rename(ang[0],'/home/tanner/src/wnpy2/thermal/data/angThermal.asc')
    
def extractZip():
    print "extracting KMLs from ZIP..."
    with zipfile.ZipFile('/home/tanner/src/wnpy2/thermal/pThermal.zip',"r") as z:
        z.extractall('/home/tanner/src/wnpy2/thermal/data')

def renameZipExtracts():
    print "renaming zip files..."
    kmlGrid=glob.glob('/home/tanner/src/wnpy2/thermal/data/poph_*.kml')
    key=glob.glob('/home/tanner/src/wnpy2/thermal/data/poph_*_stability.bmp')
    time=glob.glob('/home/tanner/src/wnpy2/thermal/data/poph_*.date_time.bmp')
    os.rename(kmlGrid[0],'/home/tanner/src/wnpy2/thermal/data/pThermal.kml')
    os.rename(key[0],'/home/tanner/src/wnpy2/thermal/data/pThermal.bmp')
    os.rename(time[0],'/home/tanner/src/wnpy2/thermal/data/PDS.bmp')
        
# NCRM8, TS673, PHYM8
#2,13,   28,6,  18,28
def writeVelocityFile():
    print "writing Velocity Data to CSV..."
    info=time.time()
    m=list(csv.reader(open('/home/tanner/src/wnpy2/d.csv','rb')))
    vel=list(csv.reader(open('/home/tanner/src/wnpy2/thermal/data/velThermal.asc','rb'),delimiter='\t'))
    
    nnNCRM8=vel[41][14]
    nnTS673=vel[14][6]
    nnPHYM8=vel[24][28]
    PHYM8=m[1][7]
    TS673=m[2][7]
    NCRM8=m[3][7]
    
    with open('/home/tanner/src/wnpy2/thermal/data/ThermalVelocity.csv','a') as csvfile:
        blue=csv.writer(csvfile,delimiter=',')
        dat=[info,NCRM8,nnNCRM8,TS673,nnTS673,PHYM8,nnPHYM8]
        blue.writerow(dat)

def writeAngleFile():
    print "writing Angle Data to CSV..."
    info=time.time()
    m=list(csv.reader(open('/home/tanner/src/wnpy2/d.csv','rb')))
    vel=list(csv.reader(open('/home/tanner/src/wnpy2/thermal/data/angThermal.asc','rb'),delimiter='\t'))
    
    nnNCRM8=vel[41][14]
    nnTS673=vel[14][6]
    nnPHYM8=vel[24][28]
    PHYM8=m[1][9]
    TS673=m[2][9]
    NCRM8=m[3][9]
    
    with open('/home/tanner/src/wnpy2/thermal/data/ThermalAngle.csv','a') as csvfile:
        blue=csv.writer(csvfile,delimiter=',')
        dat=[info,NCRM8,nnNCRM8,TS673,nnTS673,PHYM8,nnPHYM8]
        blue.writerow(dat)
def moveLocalFiles():
    print "moving thermal Sim Files to ninjaoutput..."
    shutil.copyfile('/home/tanner/src/wnpy2/thermal/data/pThermal.bmp','/home/tanner/ninjaoutput/thermal/pThermal.bmp')
    shutil.copyfile('/home/tanner/src/wnpy2/thermal/data/pThermal.kml','/home/tanner/ninjaoutput/thermal/pThermal.kml')
    shutil.copyfile('/home/tanner/src/wnpy2/thermal/data/PDS.bmp','/home/tanner/ninjaoutput/diurnal/PDS.bmp')
def runThermal2():
    master=getTime()
    writeWNcfg(master)
    runWN()
    renameFiles()
    extractZip()
    renameZipExtracts()
    writeVelocityFile()
    writeAngleFile()
    moveLocalFiles()
