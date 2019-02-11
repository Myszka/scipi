#!/usr/bin/python
from datetime import datetime,timedelta
import time
import os
import os.path
import serial
import pynmea2
import signal

datadir='/var/data/GPS'
filenm='gps'
IDstacji=30100

def initgps(sport):
    try:
        ser = serial.Serial(sport,9600)
        seria = 1
        return ser
    except:
        seria = 0
        print "No GPS"
        return 99


def getgps(ser):
	#try:
		crA=0
		crB=0
		ser.flushInput()
		ser.flushOutput()

		while (crA+crB<2):
			data = ser.readline()
			if (data.startswith("$GPRMC")):
				msg1=pynmea2.parse(data)
				crA=1

			if (data.startswith("$GPGGA")):
				msg2=pynmea2.parse(data)
				crB=1
                
		dane=[msg1.datetime,msg2.latitude,msg2.longitude,msg2.altitude]
		return dane

	#except:
		#print "GPS data error"
		#return 99

def filetowrite():
    directory=datadir+'/' + datetime.utcnow().strftime("%Y%m")
    if not os.path.exists(directory):
     os.makedirs(directory)
    name="/"+filenm+'_'+datetime.utcnow().isoformat()[:10]+".csv"
    fname=directory + name
    if os.path.isfile(fname)==False:
        f = open(fname,'w')
        f.write("'timestamp','YEARgps','MONTHgps','DAYgps','HOURgps','MINUTEgps','SECONDgps','Lat','Long','Alt'\n")
        f.close()
    return fname


def exiter():
	sergps.close()
	print "End of measurements"
	return 0

#Init
signal.signal(signal.SIGTERM, exiter)
sergps=initgps('/dev/ttyS2')

#Run Sampling


while True:
    try:
        fname=filetowrite()
        danegps=getgps(sergps)
        with open(fname, 'a') as f:
            f.write(str(time.time())+','+str(danegps[0].year)+','+str(danegps[0].month)+','+str(danegps[0].day)+','+str(danegps[0].hour)+','+str(danegps[0].minute)+','+str(danegps[0].second)+','+str(danegps[1])+','+str(danegps[2])+','+str(danegps[3])+'\n')

        f.closed
        print 'time '+str(danegps[0].hour)+':'+str(danegps[0].minute)+':'+str(danegps[0].second)+'x='+str(danegps[2])+'y='+str(danegps[1])+' Alt: '+str(danegps[3]) 

    except:
        exiter()
