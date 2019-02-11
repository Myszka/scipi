#!/usr/bin/python
import serial
import smbus
import time
import gzip
import requests
import struct
import array
import time
import io, fcntl
from datetime import datetime,timedelta
import os

datadir='/var/data/METEO'
filenm='meteo'
IDstacji=40108


def initserial(port='/dev/ttyS1'):
        '''
        Initialize serial port for Meteo Station
        '''
        try:
                ser = serial.Serial(port, 19200)
                ser.flushInput()
                ser.flushOutput()
                return ser
        except Exception as e:
                print ("Serial initialization error: {}".format(e))
                return 99

def readmeteo(serial):
        '''
        Read data from Meteo
        '''
        try:
				dane=serial.readline()

				ser.flushInput()
				ser.flushOutput()

				meteo=dane.split(',')[1:-2]
				U=meteo[0]
				V=meteo[1]
				p=meteo[2]
				temp=meteo[3]
				rh=meteo[4]
				td=meteo[5]
				volt=meteo[6]

				return [U,V,p,temp,rh,td,volt]

        except Exception as e:
                print ("Meteo data read error: {}".format(e))
                return 1


def toascii(inp):
        '''
        Function to convert tables to ascii string lines
        '''
        out=''
        for i in inp:
                out=out+str(i)+','
        return out

def timestr():
        '''
        Return time string formated for the project
        '''
        return time.strftime('%Y,%m,%d,%H,%M,%S,', time.gmtime())


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
        f.write("'YEAR','MONTH','DAY','HOUR','MINUTE','SECOND','TIME','U','V','Pressure,'Temperature','Humidity','TD','Voltage'\n")
        f.close()
    return fname



ser=initserial()
inittime=datetime.now().second

while True:
        if inittime!=datetime.now().second:
                inittime=datetime.now().second
                print datetime.now().isoformat()
                try:
                        meteo=readmeteo(ser)
                        print meteo
                        time.sleep(0.1)

                        if len(meteo)>1:
                                fname=filetowrite()
                                with open(fname, 'a') as f:
                                	f.write(str(IDstacji)+','+str(datetime.utcnow().year)+','+str(datetime.utcnow().month)+','+str(datetime.utcnow().day)+','+str(datetime.utcnow().hour)+','+str(datetime.utcnow().minute)+','+str(datetime.utcnow().second)+','+str(date2matlab(datetime.now()))+','+toascii(meteo)+'\n')
                                	f.closed

                        else:
                                ser.close()
                                ser=initserial()
                except Exception as e:
                        ser.close()
                        ser=initserial()
                        print "ERROR"

