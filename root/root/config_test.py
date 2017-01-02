import yaml
import requests

import esx_snmp
import synology_snmp
import ups_snmp
import misc_ipmi

import host_classes as host
import handlers as func

import time
import datetime
import math



# starttime=time.time()

SECONDS = 30.0

def roundTimeToSeconds(unixTime,secondsToRound):
	return int(round(unixTime / secondsToRound) * secondsToRound)

with open("../config/config.yaml", 'r') as stream:
	try:
		config = yaml.load(stream)
	except yaml.YAMLError as exc:
		print(exc)
		
while True:
	print("Gathering statistics every "+str(SECONDS)+" seconds")
	# timeTest = int(round(time.time() / SECONDS) * SECONDS)
	# timeTest = (math.ceil(time.time() / SECONDS))*SECONDS
	# timeTest = (math.ceil(time.time() / SECONDS))*SECONDS
	timeStamp = roundTimeToSeconds(time.time(),SECONDS)

	print("Actual Time:",datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	print("Timestamp:",datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S'))

	INFLUXDB_CONFIG = config["influxdb"]
	ESXI_HOSTS = config["esxi_hosts"]
	IPMI_HOSTS = config["ipmi_hosts"]
	SYNOLOGY_HOSTS = config["synology_hosts"]
	UPS_HOSTS = config["ups_hosts"]

	valueInsertList = []

	for hostData in ESXI_HOSTS:
		esxHost = host.EsxHost(hostData["hostname"],hostData["community"],hostData["version"])
		valueInsertList = esx_snmp.procLoad(esxHost,valueInsertList,timeStamp)
		valueInsertList = esx_snmp.VMList(esxHost,valueInsertList,timeStamp)

	for hostData in IPMI_HOSTS:
		ipmiHost = host.IpmiHost(hostData["hostname"],hostData["username"],hostData["password"])
		valueInsertList = misc_ipmi.fanTempMeasure(ipmiHost,valueInsertList,timeStamp)

	for hostData in SYNOLOGY_HOSTS:
		synHost = host.SynologyHost(hostData["hostname"],hostData["community"],hostData["version"],hostData["volumes"])
		valueInsertList = synology_snmp.diskUsage(synHost,valueInsertList,timeStamp)
		valueInsertList = synology_snmp.diskTemp(synHost,valueInsertList,timeStamp)

	for hostData in UPS_HOSTS:
		upsHost = host.UpsHost(hostData["hostname"],hostData["community"],hostData["version"])
		# print(upsHost.hostname)
		valueInsertList = ups_snmp.upsPower(upsHost,valueInsertList,timeStamp)
		# valueInsertList.append(func.getPostData(INFLUXDB_CONFIG,measurementData,timeStamp))

	length = len(valueInsertList) - 1
	data = ""
	if length == 0:
		data = valueInsertList[0]
	else:
		for value in valueInsertList[:-1]:
			data = data+value+"\n"
			# print(value)
		pass
		data = data+valueInsertList[length]


	print(data)

	INFLUX_SERVER = str(INFLUXDB_CONFIG["hostname"])
	INFLUX_PORT = str(INFLUXDB_CONFIG["port"])
	INFLUX_DB = str(INFLUXDB_CONFIG["database"])
	url = "http://"+INFLUX_SERVER+":"+INFLUX_PORT+"/write?db="+INFLUX_DB+"&precision=s"
	requests.post(url, data=data,headers={'Content-Type': 'application/octet-stream'},timeout = 3)

	timeToSleep = SECONDS - ((time.time() - timeStamp) % SECONDS)
	print("Statistics gathered, sleeping for "+str(timeToSleep)+" seconds")
	time.sleep(timeToSleep)
	pass