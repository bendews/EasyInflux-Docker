import yaml

import esx_snmp
import synology_snmp
import ups_snmp
import misc_ipmi

import time
import datetime
import math


# starttime=time.time()

SECONDS = 30.0

def roundTimeToSeconds(unixTime,secondsToRound):
	return int(round(unixTime / secondsToRound) * secondsToRound)

with open("config.yaml", 'r') as stream:
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

	for hostData in ESXI_HOSTS:
		esx_snmp.procLoad(INFLUXDB_CONFIG,hostData,timeStamp)
		esx_snmp.VMList(INFLUXDB_CONFIG,hostData,timeStamp)

	for hostData in IPMI_HOSTS:
		misc_ipmi.fanTempMeasure(INFLUXDB_CONFIG,hostData,timeStamp)

	for hostData in SYNOLOGY_HOSTS:
		synology_snmp.diskUsage(INFLUXDB_CONFIG,hostData,timeStamp)
		synology_snmp.diskTemp(INFLUXDB_CONFIG,hostData,timeStamp)

	for hostData in UPS_HOSTS:
		ups_snmp.upsPower(INFLUXDB_CONFIG,hostData,timeStamp)

	timeToSleep = SECONDS - ((time.time() - timeStamp) % SECONDS)
	print("Statistics gathered, sleeping for "+str(timeToSleep)+" seconds")
	time.sleep(timeToSleep)
	pass