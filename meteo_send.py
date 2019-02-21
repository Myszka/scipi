from datetime import datetime,timedelta
from numpy import genfromtxt,mean,isnan
from Adafruit_IO import Client
from time import sleep
from sendcfg import aio

datadir='/var/data/'
fol='PMS7003'
fil='pms7003'

def date2matlab(dt):
   ord = dt.toordinal()
   mdn = dt + timedelta(days = 366)
   frac = (dt-datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
   return mdn.toordinal() + frac

while True:
    try:
        #folder
        fold=datetime.now().strftime('%Y%m')

        #file
        fild=datetime.now().strftime('%Y-%m-%d')
        
        #path
        path=datadir+fol+'/'+fold+'/'+fil+'_'+fild+'.csv'

        data=genfromtxt(path,skip_header=1,delimiter=',')
    except:
        print "ERROR: no file or file corrupted"

    try:
        inT=date2matlab(datetime.now()-timedelta(minutes=1))
        
        #column number for matlab time
        seldata=data[data[:,6]>inT,:]
        #column number for temperature
        pm25=mean(seldata[:,8])
        #column number for humidity
        pm10=mean(seldata[:,9])
        #column number for pressure
        print(str(pm25)+" PM 2.5")
        print(str(pm10)+" PM 10")
    except:
        print "ERROR: data processing wrong"

    try:
        if ~isnan(pm25):
            aio.send('bielskobiala.bbup-pm25', pm25)
            print(str(temp)+" PM 2.5 sent to IO")
            aio.send('bielskobiala.bbup-pm10', pm10)
            print(str(humid)+" PM 10 sent to IO")
            
        else:
            print("No new data")
    except:
        print "ERROR: data sending"

    sleep(55)
