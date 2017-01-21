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

def upsPower(upsHost,influx):
	upsInfoOID = "1.3.6.1.2.1.33.1"
	upsWattsOID = upsInfoOID+".4.4.1.4.1"
	upsMinutesOID = upsInfoOID+".2.3.0"
	upsChargeOID = upsInfoOID+".2.4.0"

	hostname = upsHost.hostname
	snmpCommunity = upsHost.snmpCommunity
	snmpVersion = upsHost.snmpVersion

	output = upsHost.snmpWalk(upsInfoOID)

	for line in output:
		if upsWattsOID in line:
			result = re.findall(r'\: (\d*)',line)
			upsPower = str(result[0])
			data_upsPower = [hostname,"ActivePower","ups_power",upsPower]
			influx.append_measurement(data_upsPower)
		pass
		if upsMinutesOID in line:
			result = re.findall(r'\: (\d*)',line)
			upsPower = str(result[0])
			data_upsPower = [hostname,"MinutesRemaining","ups_power",upsPower]
			influx.append_measurement(data_upsPower)
		pass
		if upsChargeOID in line:
			result = re.findall(r'\: (\d*)',line)
			upsPower = str(result[0])
			data_upsPower = [hostname,"ChargePercent","ups_power",upsPower]
			influx.append_measurement(data_upsPower)
		pass
	pass