"""
Automating a stupid fix that should have been done long ago. If the file breaks, just run this with the correct iterator

"""


import shutil
import os

numIter=7

##########
#Standard#
##########


SAcsv='/home/tanner/src/wnpy2/standard/data/OldData/SAng'+str(numIter)+'.csv'
os.rename('/home/tanner/src/wnpy2/standard/data/StandardAngle.csv',SAcsv)

SVcsv='/home/tanner/src/wnpy2/standard/data/OldData/SVel'+str(numIter)+'.csv'
os.rename('/home/tanner/src/wnpy2/standard/data/StandardVelcotiy.csv',SVcsv)

# shutil.copyfile('/home/tanner/src/wxPy/wxLog.txt','/home/tanner/wnwebsrc/trombones/testDir/wxLog.txt')

shutil.copyfile('/home/tanner/src/wnpy2/blanks/StandardAngle.csv','/home/tanner/src/wnpy2/standard/data/StandardAngle.csv')
shutil.copyfile('/home/tanner/src/wnpy2/blanks/StandardVelcotiy.csv','/home/tanner/src/wnpy2/standard/data/StandardVelocity.csv')

#########
#Diurnal#
#########

os.rename('/home/tanner/src/wnpy2/diurnal/data/DiurnalAngle.csv', '/home/tanner/src/wnpy2/diurnal/data/OldData/DAng'+str(numIter)+'.csv')
os.rename('/home/tanner/src/wnpy2/diurnal/data/DiurnalVelocity.csv', '/home/tanner/src/wnpy2/diurnal/data/OldData/DVel'+str(numIter)+'.csv')

shutil.copyfile('/home/tanner/src/wnpy2/blanks/DiurnalAngle.csv', '/home/tanner/src/wnpy2/diurnal/data/DiurnalAngle.csv')
shutil.copyfile('/home/tanner/src/wnpy2/blanks/DiurnalVelocity.csv', '/home/tanner/src/wnpy2/diurnal/data/DiurnalVelocity.csv')

###########
#Stability#
###########

os.rename('/home/tanner/src/wnpy2/stability/data/StabilityAngle.csv', '/home/tanner/src/wnpy2/stability/data/OldData/SAng'+str(numIter)+'.csv')
os.rename('/home/tanner/src/wnpy2/stability/data/StabilityVelocity.csv', '/home/tanner/src/wnpy2/stability/data/OldData/SVel'+str(numIter)+'.csv')

shutil.copyfile('/home/tanner/src/wnpy2/blanks/StabilityAngle.csv', '/home/tanner/src/wnpy2/stability/data/StabilityAngle.csv')
shutil.copyfile('/home/tanner/src/wnpy2/blanks/StabilityVelocity.csv', '/home/tanner/src/wnpy2/stability/data/StabilityVelocity.csv')

#########
#Thermal#
#########

os.rename('/home/tanner/src/wnpy2/thermal/data/ThermalAngle.csv', '/home/tanner/src/wnpy2/thermal/data/OldData/TAng'+str(numIter)+'.csv')
os.rename('/home/tanner/src/wnpy2/stability/data/ThermalVelocity.csv', '/home/tanner/src/wnpy2/thermal/data/OldData/TVel'+str(numIter)+'.csv')

shutil.copyfile('/home/tanner/src/wnpy2/blanks/ThermalAngle.csv', '/home/tanner/src/wnpy2/thermal/data/ThermalAngle.csv')
shutil.copyfile('/home/tanner/src/wnpy2/blanks/ThermalVelocity.csv', '/home/tanner/src/wnpy2/thermal/data/ThermalVelocity.csv')
