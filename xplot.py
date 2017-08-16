import plot2

#MAKE PLOTS
stepdata=plot2.CreateSteps()
stationData=plot2.AssembleData()
plot2.plotVelocity("/home/tanner/ninjaoutput/thermal/NCRM8.png","NCRM8",0,2,"A",stationData,stepdata)
plot2.plotVelocity("/home/tanner/ninjaoutput/thermal/TS673.png","TS673",1,2,"A",stationData,stepdata)
plot2.plotVelocity("/home/tanner/ninjaoutput/thermal/PHYM8.png","PHYM8",2,2,"A",stationData,stepdata)

