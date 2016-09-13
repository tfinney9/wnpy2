# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 12:57:48 2016

@author: tanner
"""

import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
import numpy
import datetime
import time

# dat=[info,NCRM8,nnNCRM8,TS673,nnTS673,PHYM8,nnPHYM8]
def readTime():
    valData=list(csv.reader(open('/home/tanner/src/wnpy2/standard/data/StandardVelocity.csv','r'),delimiter=','))
    tStep=list()    
    dA=list()    
    for i in range(len(valData)):
        tStep.append(float(valData[i][0]))
    for k in range(len(tStep)):
        dA.append(datetime.datetime.fromtimestamp(tStep[k]))
    return dA        
    
def readStep():
    valData=list(csv.reader(open('/home/tanner/src/wnpy2/standard/data/StandardVelocity.csv','r'),delimiter=','))
    tStep=list()   
    for i in range(len(valData)):
        tStep.append(float(valData[i][0]))
    return tStep
    

def readObservedData():
    valData=list(csv.reader(open('/home/tanner/src/wnpy2/standard/data/StandardVelocity.csv','r'),delimiter=','))
    NCRM8=list()
    TS673=list()
    PHYM8=list()
    obs=list()
    
    for i in range(len(valData)):
        NCRM8.append(float(valData[i][1]))
        TS673.append(float(valData[i][3]))
        PHYM8.append(float(valData[i][5]))
        
    obs.append(NCRM8)
    obs.append(TS673)
    obs.append(PHYM8)
    
    return obs



def readStandardData():
    valData=list(csv.reader(open('/home/tanner/src/wnpy2/standard/data/StandardVelocity.csv','r'),delimiter=','))
    NCRM8=list()
    TS673=list()
    PHYM8=list()
    obs=list()
    
    for i in range(len(valData)):
        NCRM8.append(float(valData[i][2]))
        TS673.append(float(valData[i][4]))
        PHYM8.append(float(valData[i][6]))
        
    obs.append(NCRM8)
    obs.append(TS673)
    obs.append(PHYM8)
    
    return obs
    
def readDiurnalData():
    valData=list(csv.reader(open('/home/tanner/src/wnpy2/diurnal/data/DiurnalVelocity.csv','r'),delimiter=','))
    NCRM8=list()
    TS673=list()
    PHYM8=list()
    obs=list()
    
    for i in range(len(valData)):
        NCRM8.append(float(valData[i][2]))
        TS673.append(float(valData[i][4]))
        PHYM8.append(float(valData[i][6]))
    obs.append(NCRM8)
    obs.append(TS673)
    obs.append(PHYM8)
    
    return obs

def readStabilityData():
    valData=list(csv.reader(open('/home/tanner/src/wnpy2/stability/data/StabilityVelocity.csv','r'),delimiter=','))
    NCRM8=list()
    TS673=list()
    PHYM8=list()
    obs=list()
    
    for i in range(len(valData)):
        NCRM8.append(float(valData[i][2]))
        TS673.append(float(valData[i][4]))
        PHYM8.append(float(valData[i][6]))
    obs.append(NCRM8)
    obs.append(TS673)
    obs.append(PHYM8)
    
    return obs
    
def readThermalData():
    valData=list(csv.reader(open('/home/tanner/src/wnpy2/thermal/data/ThermalVelocity.csv','r'),delimiter=','))
    NCRM8=list()
    TS673=list()
    PHYM8=list()
    obs=list()
    
    for i in range(len(valData)):
        NCRM8.append(float(valData[i][2]))
        TS673.append(float(valData[i][4]))
        PHYM8.append(float(valData[i][6]))
    obs.append(NCRM8)
    obs.append(TS673)
    obs.append(PHYM8)
    
    return obs
def CreateSteps():
    steps=readStep()
    init=steps[0]-3600
    final=steps[-1]+3600
    
    dInit=datetime.datetime.fromtimestamp(init)
    dFinal=datetime.datetime.fromtimestamp(final)
    
    steplist=list()
    steplist.append(dInit)
    steplist.append(dFinal)

    return steplist    
    
        
def AssembleData(): 
    total=list()       
    plotTime=readTime()
    observed=readObservedData()
    standard=readStandardData()
    diurnal=readDiurnalData()
    stability=readStabilityData()
    thermal=readThermalData()
    
    total.append(plotTime)
    total.append(observed)
    total.append(standard)
    total.append(diurnal)
    total.append(stability)
    total.append(thermal)
    
    
#    init=steps[0]-3600
#    final=steps[-1]+3600
#    
#    dInit=datetime.datetime.fromtimestamp(init)
#    dFinal=datetime.datetime.fromtimestamp(final)
    
    return total
    
def plotVelocity(fileName,stationID,idx0,idx1,ID,data,steps):
    q=0
    pyplot.figure(idx0)
    print "making plot for: ",stationID
#        pyplot.plot(dA,total[idx0],marker='o',color='m',ls='-',label="Observed Data for %s" % stationID)

#   pyplot.plot(dA,total[idx1],color='r',marker='o',markeredgecolor='r',markerfacecolor='none',linestyle='--',label="WindNinja Simulation with Thermal Parameters")
#    pyplot.plot(dA,total[4],marker='.',color='c',ls='-',label="Initialized Point: PHYM8")
#    if ska==True:
#        pyplot.plot(dA,stable[idx1],color='y',marker='o',markeredgecolor='y',markerfacecolor='none',ls='--',label='nonDiurnal, neutral WN Sim')


    pyplot.plot(data[0],data[1][idx0],marker='o',color='m',ls='-',label='Observed Data for %s'% stationID)
    pyplot.plot(data[0],data[2][idx0],color='y',marker='o',markeredgecolor='y',markerfacecolor='none',ls='--',label='Standard Simulation')
    pyplot.plot(data[0],data[3][idx0],color='b',marker='o',markeredgecolor='b',markerfacecolor='none',ls='--',label='+Diurnal Winds')
    pyplot.plot(data[0],data[4][idx0],color='g',marker='o',markeredgecolor='g',markerfacecolor='none',ls='--',label='+Non-neutral Stability')
    pyplot.plot(data[0],data[5][idx0],color='r',marker='o',markeredgecolor='r',markerfacecolor='none',ls='--',label='+Both Thermal Params')
    pyplot.legend(bbox_to_anchor=(0.0,1.4),loc='upper right',borderaxespad=0)
    pyplot.ylabel('Wind Speed (m/s)')
    pyplot.title('Diurnal Non-Neutral Stability Wind\n Speed Validation for %s' % stationID, loc='right')
    pyplot.xlabel('Time')
    
    
    pyplot.grid()    
    
    pyplot.xticks(rotation=45)
    
    pyplot.ylim(-3.0)
    pyplot.xlim(steps[0],steps[1])
    
    pyplot.savefig(fileName,bbox_inches='tight')

    
    return q
    
    
    



#stepdata=CreateSteps()
#stationData=AssembleData()
#plotVelocity("/home/tanner/ninjaoutput/thermal/NCRM8.png","NCRM8",0,2,"A",stationData,stepdata)
#plotVelocity("/home/tanner/ninjaoutput/thermal/TS673.png","TS673",1,2,"A",stationData,stepdata)
#plotVelocity("/home/tanner/ninjaoutput/thermal/PHYM8.png","PHYM8",2,2,"A",stationData,stepdata)
