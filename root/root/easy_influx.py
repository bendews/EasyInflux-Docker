################################
#  - Ben Dews
#  - bendews.com
#  - 02/01/2017
#  - Main loop for EasyInflux script
################################

import yaml
import requests
import logging
import os
import time
import datetime
import math

import esx_snmp
import synology_snmp
import ups_snmp
import misc_ipmi

import host_classes as host
import handlers as func


currentDirectory = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.DEBUG)

# Round unix time to closest interval period
def roundTimeToSeconds(unixTime,secondsToRound):
	return int(round(unixTime / secondsToRound) * secondsToRound)

def listToInfluxDBString(list):
	length = len(list) - 1
	influxDBString = ""
	if length == 0:
		influxDBString = list[0]
	else:
		for value in list[:-1]:
			influxDBString = influxDBString+value+"\n"
		pass
		influxDBString = influxDBString+list[length]
	return influxDBString

# Load config file
with open(currentDirectory+"/../config/config.yaml", 'r') as stream:
	try:
		config = yaml.load(stream)
	except yaml.YAMLError as exc:
		logging.error(exc)
		exit()

# Assign InfluxDB Variables
INFLUXDB_CONFIG = config["influxdb"]
# Interval to run script
INSERT_INTERVAL = float(INFLUXDB_CONFIG["insert_interval"])
# hostname of influxDB server
INFLUX_SERVER = str(INFLUXDB_CONFIG["hostname"])
# API port of influxDB server
INFLUX_PORT = str(INFLUXDB_CONFIG["port"])
# Database for values to be inserted into
INFLUX_DB = str(INFLUXDB_CONFIG["database"])
# URL used for POST request
INFLUX_URL = "http://"+INFLUX_SERVER+":"+INFLUX_PORT+"/write?db="+INFLUX_DB+"&precision=s"
		
while True:
	# Round insert timestamp to interval period
	timeStamp = roundTimeToSeconds(time.time(),INSERT_INTERVAL)
	logging.debug("Gathering statistics every "+str(INSERT_INTERVAL)+" seconds")
	logging.debug("Actual Time:"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	logging.debug("Timestamp for data:"+datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S'))

	if "esxi_hosts" in config:
		ESXI_HOSTS = config["esxi_hosts"]
		pass
	if "ipmi_hosts" in config:
		IPMI_HOSTS = config["ipmi_hosts"]
		pass
	if "synology_hosts" in config:
		SYNOLOGY_HOSTS = config["synology_hosts"]
		pass
	if "ups_hosts" in config:
		UPS_HOSTS = config["ups_hosts"]
		pass

	valueList = []

	for hostData in ESXI_HOSTS:
		esxHost = host.EsxHost(hostData["hostname"],hostData["snmp_community"],hostData["snmp_version"])
		valueList = esx_snmp.procLoad(esxHost,valueList,timeStamp)
		valueList = esx_snmp.VMList(esxHost,valueList,timeStamp)

	for hostData in IPMI_HOSTS:
		ipmiHost = host.IpmiHost(hostData["hostname"],hostData["ipmi_username"],hostData["ipmi_password"])
		valueList = misc_ipmi.fanTempMeasure(ipmiHost,valueList,timeStamp)

	for hostData in SYNOLOGY_HOSTS:
		synHost = host.SynologyHost(hostData["hostname"],hostData["snmp_community"],hostData["snmp_version"],hostData["volumes"])
		valueList = synology_snmp.diskUsage(synHost,valueList,timeStamp)
		valueList = synology_snmp.diskTemp(synHost,valueList,timeStamp)

	for hostData in UPS_HOSTS:
		upsHost = host.UpsHost(hostData["hostname"],hostData["snmp_community"],hostData["snmp_version"])
		valueList = ups_snmp.upsPower(upsHost,valueList,timeStamp)

	# Convert list of insert data into string for POST request
	INFLUX_DATA = listToInfluxDBString(valueList)
	# Print collected data
	logging.debug(INFLUX_DATA)
	requests.post(INFLUX_URL, data=INFLUX_DATA,headers={'Content-Type': 'application/octet-stream'},timeout = 3)

	# Delay data collection loop to match interval period
	timeToSleep = INSERT_INTERVAL - ((time.time() - timeStamp) % INSERT_INTERVAL)
	logging.info("Statistics gathered, sleeping for "+str(timeToSleep)+" seconds")
	time.sleep(timeToSleep)
	pass