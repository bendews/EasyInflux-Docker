################################
#  - Ben Dews
#  - bendews.com
#  - 30/12/2016
#  - Script to get ESXi SNMP statistics and insert to InfluxDB
################################
import subprocess
import requests
import re

import handlers as func

def procLoad(esxHost,influx):
	procOID = ".1.3.6.1.2.1.25.3.3.1.2"
	i = 0

	hostname = esxHost.hostname
	snmpCommunity = esxHost.snmpCommunity
	snmpVersion = esxHost.snmpVersion


	output = esxHost.snmpWalk(procOID)
	for line in output:
		if procOID in line:
			i += 1
			cpuCore = "cpu"+str(i)
			result = re.findall(r'\: (\d*)',line)
			if result:
				loadValue = str(result[0])
				data_procLoad = [hostname,cpuCore,"cpu_load",loadValue]
				influx.append_measurement(data_procLoad)
			pass
		pass

def VMList(esxHost,influx):
	vmInfoOID = ".1.3.6.1.4.1.6876.2.1.1"
	vmLabelOID = vmInfoOID+".2"
	vmStateOID = vmInfoOID+".6"
	vmNames = []
	powerStates = []

	hostname = esxHost.hostname
	snmpCommunity = esxHost.snmpCommunity
	snmpVersion = esxHost.snmpVersion

	output = esxHost.snmpWalk(vmInfoOID)

	for line in output:
		if vmLabelOID in line:
			result = re.findall(r'\: (.*)',line)
			result = str(result[0])
			result = result.replace('"','')
			vmNames.append(result)
			pass
		if vmStateOID in line:
			result = re.findall(r'\: (.*)',line)
			result = str(result[0])
			result = result.replace('"','')
			powerStates.append(result)
			pass
		pass
	for name,state in zip(vmNames,powerStates):
		binaryState = 1 if state =="powered on" else 0
		data_VMStates = [hostname,name,"vm_state",binaryState]
		influx.append_measurement(data_VMStates)
	pass
