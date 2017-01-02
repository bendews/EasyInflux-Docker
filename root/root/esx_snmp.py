################################
#  - Ben Dews
#  - bendews.com
#  - 30/12/2016
#  - Script to get IPMI statistics and insert to InfluxDB
################################
import subprocess
import requests
import re

def writeData(influxServerData,measurementData,timeStamp):
	INFLUX_SERVER = str(influxServerData["hostname"])
	INFLUX_PORT = str(influxServerData["port"])
	INFLUX_DB = str(influxServerData["database"])

	host = str(measurementData[0]).replace(" ", "")
	device = str(measurementData[1]).replace(" ", "")
	item = str(measurementData[2]).replace(" ", "")
	value = str(measurementData[3]).replace(" ", "")

	url = "http://"+INFLUX_SERVER+":"+INFLUX_PORT+"/write?db="+INFLUX_DB+"&precision=s"
	data = "snmp_data,device="+device+",host="+host+",sensor="+item+" value="+value+" "+str(timeStamp)
	requests.post(url, data=data,headers={'Content-Type': 'application/octet-stream'},timeout = 3)
	pass

def snmpWalk(hostData,oid):
	SNMP_SERVER = hostData['hostname']
	SNMP_COMMUNITY = hostData['community']

	p = subprocess.run(["snmpwalk", "-O", "fn", "-v", "2c", "-c", SNMP_COMMUNITY, SNMP_SERVER, oid], stdout=subprocess.PIPE)
	output = p.stdout.decode('utf8').splitlines()
	return output
	pass

def procLoad(influxData,hostData,timeStamp):
	procOID = ".1.3.6.1.2.1.25.3.3.1.2"
	i = 0
	output = snmpWalk(hostData,procOID)
	for line in output:
		if procOID in line:
			i += 1
			cpuCore = "cpu"+str(i)
			result = re.findall(r'\: (\d*)',line)
			loadValue = str(result[0])
			data_procLoad = [hostData['hostname'],cpuCore,"cpu_load",loadValue]
			writeData(influxData,data_procLoad,timeStamp)
			# print(cpuCore,loadValue)
			pass
		pass

def VMList(influxData,hostData,timeStamp):
	vmNames = []
	powerStates = []

	output = snmpWalk(hostData,".1.3.6.1.4.1.6876.2.1.1")

	for line in output:
		if ".1.3.6.1.4.1.6876.2.1.1.2." in line:
			result = re.findall(r'\: (.*)',line)
			result = str(result[0])
			result = result.replace('"','')
			vmNames.append(result)
			pass
		if ".1.3.6.1.4.1.6876.2.1.1.6." in line:
			result = re.findall(r'\: (.*)',line)
			result = str(result[0])
			result = result.replace('"','')
			powerStates.append(result)
			pass
		pass
	for name,state in zip(vmNames,powerStates):
		binaryState = 1 if state =="powered on" else 0
		data_VMStates = [hostData['hostname'],name,"vm_state",binaryState]
		writeData(influxData,data_VMStates,timeStamp)
		print(name,state)
	pass
