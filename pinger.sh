#!/bin/bash
IPserv="212.87.6.251/mich/Rover.php"
stacja='bb-rover'
while :
do
	myIP=`/bin/ip a s |grep inet|grep brd|cut -d' ' -f6|tail -1`
	datenow=`date '+%Y%m%d_%H:%M.%S'`
	folder=`date '+%Y%m/pms7003_%Y-%m-%d'`
	pm10=`tail -1 /var/data/PMS7003/$folder.csv |cut -d, -f11`
	temp=`tail -1 /var/data/PMS7003/$folder.csv |cut -d, -f19`
	
	wget -T 3 -q --spider $IPserv?re=$stacja\&ip=$myIP\&dt=$datenow\&pm10=$pm10\&tm=$temp
	if [[ $? == 0 ]];
	then
		echo $? $datenow
		sleep 60
	fi
	
done
