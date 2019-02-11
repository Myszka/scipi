#!/usr/bin/env python

import spidev
import opc
import datetime, time
from datetime import datetime,timedelta
import os.path, sys, os
import serial
import signal
from time import sleep

datadir='/var/data/OPC'
filenm='opc'
IDstacji=30100

presentTime=datetime.utcnow()


# Open a SPI connection on CE0
spi = spidev.SpiDev()
spi.open(1, 0)

# Set the SPI mode and clock speed
spi.mode = 1
spi.max_speed_hz = 500000



def date2matlab(dt):
   ord = dt.toordinal()
   mdn = dt + timedelta(days = 366)
   frac = (dt-datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
   return mdn.toordinal() + frac

def filetowrite():
    directory=datadir+'/' + datetime.utcnow().strftime("%Y%m")
    if not os.path.exists(directory):
     os.makedirs(directory)
    name="/"+filenm+'_'+datetime.utcnow().isoformat()[:10]+".csv"
    fname=directory + name
    if os.path.isfile(fname)==False:
        f = open(fname,'w')
        f.write("'STATIONID','YEAR','MONTH','DAY','HOUR','MINUTE','SECOND','TIME','Bin0','Bin1','Bin2','Bin3','Bin4','Bin5','Bin6','Bin7','Bin8','Bin9','Bin10','Bin11','Bin12','Bin13','Bin14','Bin15','Bin1 MToF','Bin3 MToF','Bin5 MToF','Bin7 MToF','Checksum','PM1','PM2.5','PM10','Press','SFR','Sampling period','Temp'\n")
        f.close()
    return fname

def exiter():
	alpha.off()
	print "End of measurements"
	return 0



try:
    alpha = opc.OPCN2(spi)
except Exception as e:
    print ("Startup Error: {}".format(e))

# Turn on the OPC
alpha.on()
sleep(10)

#Run Sampling

while True:
    try:
        
        fname=filetowrite()
        hista=alpha.histogram()
        with open(fname, 'a') as f:
            f.write(str(IDstacji)+','+str(datetime.utcnow().year)+','+str(datetime.utcnow().month)+','+str(datetime.utcnow().day)+','+str(datetime.utcnow().hour)+','+str(datetime.utcnow().minute)+','+str(datetime.utcnow().second)+','+str(date2matlab(datetime.now()))+','+str(hista['Bin 0'])+','+str(hista['Bin 1'])+','+str(hista['Bin 2'])+','+str(hista['Bin 3'])+','+str(hista['Bin 4'])+','+str(hista['Bin 5'])+','+str(hista['Bin 6'])+','+str(hista['Bin 7'])+','+str(hista['Bin 8'])+','+str(hista['Bin 9'])+','+str(hista['Bin 10'])+','+str(hista['Bin 11'])+','+str(hista['Bin 12'])+','+str(hista['Bin 13'])+','+str(hista['Bin 14'])+','+str(hista['Bin 15'])+','+str(hista['Bin1 MToF'])+','+str(hista['Bin3 MToF'])+','+str(hista['Bin5 MToF'])+','+str(hista['Bin7 MToF'])+','+str(hista['Checksum'])+','+str(hista['PM1'])+','+str(hista['PM2.5'])+','+str(hista['PM10'])+','+str(hista['Pressure'])+','+str(hista['SFR'])+','+str(hista['Sampling Period'])+','+str(hista['Temperature'])+'\n')
        f.closed
        print datetime.now().isoformat()
        print hista['PM10']
        sleep(1)

    except:
        print "ERROR"
        sleep(1)

