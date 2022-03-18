#!/usr/bin/env python
from usbiss.spi import SPI
import opc
import datetime, time
from datetime import datetime,timedelta
import os.path, sys, os
import serial
import signal
from time import sleep


datadir='/var/data/OPC/'
filenm='pms7003'
interval = 60


# Open a SPI connection
spi = SPI("/dev/ttyACM0")
spi.mode = 1
spi.max_speed_hz = 500000


presentTime=datetime.utcnow()

def date2matlab(dt):
   ord = dt.toordinal()
   mdn = dt + timedelta(days = 366)
   frac = (dt-datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
   return mdn.toordinal() + frac

def filetowrite(typ=2):
#    presentTime=datetime.utcnow()
    directory=datadir + datetime.utcnow().strftime("%m%Y")
    if not os.path.exists(directory):
     os.makedirs(directory)
    if typ==2:
        name="/OPCN2_"+datetime.utcnow().isoformat()[:10]+".csv"
        fname=directory + name
        if os.path.isfile(fname)==False:
            f = open(fname,'w')
            f.write("'YEAR','MONTH','DAY','HOUR','MINUTE','SECOND','TIME','Bin0','Bin1','Bin2','Bin3','Bin4','Bin5','Bin6','Bin7','Bin8','Bin9','Bin10','Bin11','Bin12','Bin13','Bin14','Bin15','Bin1 MToF','Bin3 MToF','Bin5 MToF','Bin7 MToF','Checksum','PM1','PM2.5','PM10','Press','SFR','Sampling period','Temp'\n")
            f.close()
    elif typ==3:
        name="/OPCN3_"+datetime.utcnow().isoformat()[:10]+".csv"
        fname=directory + name
        if os.path.isfile(fname)==False:
            f = open(fname,'w')
            f.write("'YEAR','MONTH','DAY','HOUR','MINUTE','SECOND','TIME','Bin0','Bin1','Bin2','Bin3','Bin4','Bin5','Bin6','Bin7','Bin8','Bin9','Bin10','Bin11','Bin12','Bin13','Bin14','Bin15','Bin1 MToF','Bin3 MToF','Bin5 MToF','Bin7 MToF','Checksum','PM1','PM2.5','PM10','Press','SFR','Sampling period','Temp','RH','Bin16','Bin17','Bin18','Bin19','Bin20','Bin21','Bin22','Bin23' \n")
            f.close()
    return fname

def exiter():
	alpha.off()
	print "End of measurements"
	return 0

def checkOPCtype(spi):
    alpha = opc.OPCN2(spi)
    typ=alpha.read_info_string()
    if typ.find('OPC-N2') >= 0:
        return 2
    elif typ.find('OPC-N3') >= 0:
        return 3
    else:
        return -1



try:
    typ = checkOPCtype(spi)
    if typ == 2:
        alpha = opc.OPCN2(spi)
    elif typ == 3:
        alpha = opc.OPCN3(spi)
except Exception as e:
    print ("Startup Error: {}".format(e))

# Turn on the OPC
alpha.on()
sleep(60)

#Run Sampling
try:
    while True:
            fname=filetowrite(typ)
            hista=alpha.histogram()
            with open(fname, 'a') as f:
                if typ==2:
                    f.write(str(datetime.utcnow().year)+','+str(datetime.utcnow().month)+','+str(datetime.utcnow().day)+','+str(datetime.utcnow().hour)+','+str(datetime.utcnow().minute)+','+str(datetime.utcnow().second)+','+str(date2matlab(datetime.now()))+','+str(hista['Bin 0'])+','+str(hista['Bin 1'])+','+str(hista['Bin 2'])+','+str(hista['Bin 3'])+','+str(hista['Bin 4'])+','+str(hista['Bin 5'])+','+str(hista['Bin 6'])+','+str(hista['Bin 7'])+','+str(hista['Bin 8'])+','+str(hista['Bin 9'])+','+str(hista['Bin 10'])+','+str(hista['Bin 11'])+','+str(hista['Bin 12'])+','+str(hista['Bin 13'])+','+str(hista['Bin 14'])+','+str(hista['Bin 15'])+','+str(hista['Bin1 MToF'])+','+str(hista['Bin3 MToF'])+','+str(hista['Bin5 MToF'])+','+str(hista['Bin7 MToF'])+','+str(hista['Checksum'])+','+str(hista['PM1'])+','+str(hista['PM2.5'])+','+str(hista['PM10'])+','+str(hista['Pressure'])+','+str(hista['SFR'])+','+str(hista['Sampling Period'])+','+str(hista['Temperature'])+'\n')
                elif typ==3:
                    f.write(str(datetime.utcnow().year)+','+str(datetime.utcnow().month)+','+str(datetime.utcnow().day)+','+str(datetime.utcnow().hour)+','+str(datetime.utcnow().minute)+','+str(datetime.utcnow().second)+','+str(date2matlab(datetime.now()))+','+str(hista['Bin 0'])+','+str(hista['Bin 1'])+','+str(hista['Bin 2'])+','+str(hista['Bin 3'])+','+str(hista['Bin 4'])+','+str(hista['Bin 5'])+','+str(hista['Bin 6'])+','+str(hista['Bin 7'])+','+str(hista['Bin 8'])+','+str(hista['Bin 9'])+','+str(hista['Bin 10'])+','+str(hista['Bin 11'])+','+str(hista['Bin 12'])+','+str(hista['Bin 13'])+','+str(hista['Bin 14'])+','+str(hista['Bin 15'])+','+str(hista['Bin1 MToF'])+','+str(hista['Bin3 MToF'])+','+str(hista['Bin5 MToF'])+','+str(hista['Bin7 MToF'])+','+str(hista['Checksum'])+','+str(hista['PM1'])+','+str(hista['PM2.5'])+','+str(hista['PM10'])+','+str('None')+','+str(hista['Sample Flow Rate'])+','+str(hista['Sampling Period'])+','+str(hista['Temperature'])+','+str(hista['Relative humidity'])+','+str(hista['Bin 16'])+','+str(hista['Bin 17'])+','+str(hista['Bin 18'])+','+str(hista['Bin 19'])+','+str(hista['Bin 20'])+','+str(hista['Bin 21'])+','+str(hista['Bin 22'])+','+str(hista['Bin  23'])+'\n')
            f.closed
            print datetime.now().isoformat()
    	    print hista['PM2.5']
            sleep(60)

except:
    exiter()

