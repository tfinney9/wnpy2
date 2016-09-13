#!/usr/bin/env python

# NCRM8, TS673, PHYM8

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



#import diurnalAngleEval as DAE
import diurnalVelocityEval as DVE
import mwWindNinja as mw
import stableBot

def getTime():
    masterTime=list()
    masterTime.append(str(time.time()))
    masterTime.append(str(datetime.datetime.now().year))
    masterTime.append(str(datetime.datetime.now().month))
    masterTime.append(str(datetime.datetime.now().day))
    masterTime.append(str(datetime.datetime.now().hour))
    masterTime.append(str(datetime.datetime.now().minute))
    return masterTime


def fetchReal():
    print "getting weather data from MesoWest for PointInitialization"
    url=mw.stationUrlBuilder(mw.dtoken,"PHYM8",mw.var,"")
    dictData=mw.readData(url)
    mw.WriteNinjaCSV(dictData,"/home/tanner/src/wind/build/src/cli/eval/p.csv")


def fetchWeather():
    print "getting weather data from MesoWest for NCRM8, TS673, PHYM8"
    url=mw.stationUrlBuilder(mw.dtoken,"NCRM8,TS673,PHYM8",mw.var,"")
    dictData=mw.readData(url)
    mw.WriteNinjaCSV(dictData,"/home/tanner/src/wind/build/src/cli/eval/d.csv")
def writeKML():
    keyhole=open('/home/tanner/src/wind/build/src/cli/kml.cfg','w')
    keyhole.write('write_wx_station_kml        =   true\n')
    keyhole.write('wx_station_kml_filename     =   /home/tanner/src/wind/build/src/cli/eval/clark.kml\n')
    keyhole.write('wx_station_filename         =   /home/tanner/src/wind/build/src/cli/eval/d.csv\n')
    keyhole.write('elevation_file              =   /home/tanner/src/wind/build/src/cli/eval/poph.tif\n')
    keyhole.write('initialization_method       =   pointInitialization\n')
    keyhole.write('time_zone                   =   America/Denver\n')
    keyhole.close() 
    
def writeWNcfg(m):
    print "writing new cfg"
    fout = open("/home/tanner/src/wind/build/src/cli/dirnalstab.cfg", 'w')
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
    fout.write('diurnal_winds               =   true\n')
    fout.write('year                        =   %s\n' % m[1])
    fout.write('month                       =   %s\n' % m[2])
    fout.write('day                         =   %s\n' % m[3])
    fout.write('hour                        =   %s\n' % m[4])
    fout.write('minute                      =   %s\n' % m[5])
    fout.write('non_neutral_stability       =   true\n')
    fout.write('wx_station_filename         =   /home/tanner/src/wind/build/src/cli/eval/p.csv\n')
    fout.write('write_wx_station_kml        =   true\n')
    fout.write('wx_station_kml_filename     =   /home/tanner/src/wind/build/src/cli/eval/other.kml\n')
    fout.write('write_ascii_output          =   true\n')
#    if(initMethod == 'pointInitialization'):
#        fout.write('wx_station_filename         =   wxstation.csv\n')
#        fout.write('match_points                =   false\n')
#        fout.write('alpha_stability             =   %.2f\n' % alpha)
#    elif(initMethod == 'wxModelInitialization'):
#        fout.write('forecast_filename       =   %s\n' % wxFile)
    fout.close()
    
    
def makeKML():
    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wind/build/src/cli/kml.cfg'])
def runWN():
    print "Running WindNinja..."
#    subprocess32.call(['export WINDNINJA_DATA=~/src/wind/windninja/data'])
    subprocess32.call(['/home/tanner/src/wind/build/src/cli/./WindNinja_cli','/home/tanner/src/wind/build/src/cli/dirnalstab.cfg'])

def renameFile():
    print "renaming Files"
    kmz=glob.glob('/home/tanner/src/wind/build/src/cli/eval/*.kmz')
    os.rename(kmz[0],'/home/tanner/src/wind/build/src/cli/eval/PDS.zip')
    vel=glob.glob('/home/tanner/src/wind/build/src/cli/eval/*_vel.asc')
    ang=glob.glob('/home/tanner/src/wind/build/src/cli/eval/*_ang.asc')
    os.rename(vel[0],'/home/tanner/src/wind/build/src/cli/eval/velDS.asc')
    os.rename(ang[0],'/home/tanner/src/wind/build/src/cli/eval/angDS.asc')

# Important files are PDS.zip,velDS.asc,angDS.asc,d.csv

def extractZIP():
    print "extracting KMLs from ZIP"
    with zipfile.ZipFile('/home/tanner/src/wind/build/src/cli/eval/PDS.zip',"r") as z:
        z.extractall('/home/tanner/src/wind/build/src/cli/eval')
def renameZIPExtracts():
    print "renaming zip extracts"
    kmlGrid=glob.glob('/home/tanner/src/wind/build/src/cli/eval/*_stability.kml')
    key=glob.glob('/home/tanner/src/wind/build/src/cli/eval/*_stability.bmp')
    timeKey=glob.glob('/home/tanner/src/wind/build/src/cli/eval/*.date_time.bmp')
    os.rename(kmlGrid[0],'/home/tanner/src/wind/build/src/cli/eval/PDS.kml')
    os.rename(key[0],'/home/tanner/src/wind/build/src/cli/eval/PDS.bmp') 
    os.rename(timeKey[0],'/home/tanner/src/wind/build/src/cli/eval/PDSTime.bmp')    

    
# Important Files are PDS.kml, PDS.bmp, PDSTime.bmp, velDS.asc,angDS.asc,d.csv    

def moveFilesI():
    print "moving Files to stage for analysis"
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/PDS.kml','/home/tanner/src/wind/build/src/cli/eval/stage/PDS.kml')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/PDS.bmp','/home/tanner/src/wind/build/src/cli/eval/stage/PDS.bmp')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/PDSTime.bmp','/home/tanner/src/wind/build/src/cli/eval/stage/PDSTime.bmp')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/velDS.asc','/home/tanner/src/wind/build/src/cli/eval/stage/velDS.asc')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/angDS.asc','/home/tanner/src/wind/build/src/cli/eval/stage/angDS.asc')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/d.csv','/home/tanner/src/wind/build/src/cli/eval/stage/d.csv')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/clark.kml','/home/tanner/src/wind/build/src/cli/eval/stage/clark.kml')
def regularBot():
    print "running Neutral Atmosphere, non Diurnal Simulation for validation"
    stableBot.fetchReal()
    stableBot.fetchWeather()
    stableBot.writeKML()
    stableBot.writeWNcfg()
    stableBot.makeKML()
    stableBot.runWN()
    stableBot.renameFile()
    stableBot.extractZIP()
    stableBot.renameZIPExtracts()
    stableBot.writeVelocityData()
    stableBot.writeAngleData()
    
def writeAngleData():
    print "making angle plots"
    info=time.time()
    m=list(csv.reader(open('/home/tanner/src/wind/build/src/cli/eval/stage/d.csv','rb')))
    vel=list(csv.reader(open('/home/tanner/src/wind/build/src/cli/eval/stage/angDS.asc','rb'),delimiter='\t'))
    
    nnNCRM8=vel[41][14]
    nnTS673=vel[14][6]
    nnPHYM8=vel[24][28]
    PHYM8=m[1][9]
    TS673=m[2][9]
    NCRM8=m[3][9]
    
    
    with open('/home/tanner/src/wind/build/src/cli/eval/stage/diurnalAngleValidation.csv','a') as csvfile:
        blue=csv.writer(csvfile,delimiter=',')
        dat=[info,NCRM8,nnNCRM8,TS673,nnTS673,PHYM8,nnPHYM8]
        blue.writerow(dat)    
    
def writeValData():
        DVE.writeVelocityData()
        writeAngleData()



def makePlots():
    print "making validation plots"
    DVE.makePlot1('/home/tanner/src/wind/build/src/cli/eval/stage/DS-V-NCRM8.png',0,1,'NCRM8',True)
    DVE.makePlot1('/home/tanner/src/wind/build/src/cli/eval/stage/DS-V-TS673.png',2,3,'TS673',True)
    
#    DAE.makePlot1('/home/tanner/src/wind/build/src/cli/eval/stage/DS-A-NCRM8.png',0,1,'NCRM8',True)
#    DAE.makePlot1('/home/tanner/src/wind/build/src/cli/eval/stage/DS-A-TS673.png',2,3,'TS673',True)

def moveFilesII():
    print "moving files for upload"
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/stage/DS-V-TS673.png','/home/tanner/ninjaoutput/diurnal/DS-V-TS673.png')
#    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/stage/DS-A-TS673.png','/home/tanner/ninjaoutput/diurnal/DS-A-TS673.png')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/stage/DS-V-NCRM8.png','/home/tanner/ninjaoutput/diurnal/DS-V-NCRM8.png')
#    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/stage/DS-A-NCRM8.png','/home/tanner/ninjaoutput/diurnal/DS-A-NCRM8.png')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/stage/PDS.kml','/home/tanner/ninjaoutput/diurnal/PDS.kml')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/stage/clark.kml','/home/tanner/ninjaoutput/diurnal/clark.kml')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/stage/PDS.bmp','/home/tanner/ninjaoutput/diurnal/PDS.bmp')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/stage/PDSTime.bmp','/home/tanner/ninjaoutput/diurnal/PDSTime.bmp')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/regular/pRG.bmp','/home/tanner/ninjaoutput/diurnal/pRG.bmp')
    shutil.copyfile('/home/tanner/src/wind/build/src/cli/eval/regular/pRG.kml','/home/tanner/ninjaoutput/diurnal/pRG.kml')


def writeLogFile(ini):
    print "writing logfile"
    runtime=str(datetime.datetime.now().time())
    unix=str(time.time())
    log=open('/home/tanner/ninjaoutput/diurnal/DiurnalLog.txt','w')
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



master=getTime()
start=time.time()
fetchReal()
fetchWeather()
writeKML()
makeKML()
writeWNcfg(master)
runWN()
renameFile()
extractZIP()
renameZIPExtracts()
moveFilesI()
regularBot()
writeValData()
makePlots()
moveFilesII()
writeLogFile(start)









