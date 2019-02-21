from datetime import datetime,timedelta
from numpy import genfromtxt,mean,isnan
from Adafruit_IO import Client
from time import sleep
from sendcfg import aio

datadir='/var/data/'
fol='METEO'
fil='meteo'

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
        seldata=data[data[:,7]>inT,:]
        #column number for temperature
        temp=mean(seldata[:,12])
        #column number for humidity
        humid=mean(seldata[:,11])
        #column number for pressure
        press=mean(seldata[:,10])
        print(str(temp)+" C sent to IO")
        print(str(humid)+" % sent to IO")
        print(str(press)+" hPa send to IO")
    except:
        print "ERROR: data processing wrong"

    try:
        if ~isnan(temp):
            aio.send('bielskobiala.bbup-temperature', temp)
            print(str(temp)+" C sent to IO")
            aio.send('bielskobiala.bbup-humidity', humid)
            print(str(humid)+" % sent to IO")
            aio.send('bielskobiala.bbup-pressure', press)
            print(str(press)+" hPa send to IO")
            
        else:
            print("No new data")
    except:
        print "ERROR: data sending"

    sleep(55)
