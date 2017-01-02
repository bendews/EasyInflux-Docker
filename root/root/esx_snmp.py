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

def procLoad(esxHost,valueInsertList,timeStamp):
	procOID = ".1.3.6.1.2.1.25.3.3.1.2"
	i = 0

	hostname = esxHost.hostname
	snmpCommunity = esxHost.snmpCommunity
	snmpVersion = esxHost.snmpVersion


	output = func.snmpWalk(hostname,snmpCommunity,snmpVersion,procOID)
	for line in output:
		if procOID in line:
			i += 1
			cpuCore = "cpu"+str(i)
			result = re.findall(r'\: (\d*)',line)
			if result:
				loadValue = str(result[0])
				data_procLoad = [hostname,cpuCore,"cpu_load",loadValue]
				valueInsertList.append(func.getPostData(data_procLoad,timeStamp))
			pass
		pass
	return valueInsertList

def VMList(esxHost,valueInsertList,timeStamp):
	vmInfoOID = ".1.3.6.1.4.1.6876.2.1.1"
	vmLabelOID = vmInfoOID+".2"
	vmStateOID = vmInfoOID+".6"
	vmNames = []
	powerStates = []

	hostname = esxHost.hostname
	snmpCommunity = esxHost.snmpCommunity
	snmpVersion = esxHost.snmpVersion

	output = func.snmpWalk(hostname,snmpCommunity,snmpVersion,vmInfoOID)

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
		valueInsertList.append(func.getPostData(data_VMStates,timeStamp))
	pass
	return valueInsertList
