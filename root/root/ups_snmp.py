################################
#  - Ben Dews
#  - bendews.com
#  - 30/12/2016
#  - Script to get UPS SNMP and insert to InfluxDB
################################
import subprocess
import requests
import re

import handlers as func

def upsPower(upsHost,valueInsertList,timeStamp):
	upsInfoOID = "1.3.6.1.2.1.33.1"
	upsWattsOID = upsInfoOID+".4.4.1.4.1"

	hostname = upsHost.hostname
	snmpCommunity = upsHost.snmpCommunity
	snmpVersion = upsHost.snmpVersion

	output = func.snmpWalk(hostname,snmpCommunity,snmpVersion,upsInfoOID)

	for line in output:
		if upsWattsOID in line:
			result = re.findall(r'\: (\d*)',line)
			upsPower = str(result[0])
			data_upsPower = [hostname,"ActivePower","ups_power",upsPower]
			valueInsertList.append(func.getPostData(data_upsPower,timeStamp))
		pass
	pass
	return valueInsertList
