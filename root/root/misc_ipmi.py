################################
#  - Ben Dews
#  - bendews.com
#  - 30/12/2016
#  - Script to get IPMI statistics and insert to InfluxDB
################################
import subprocess
import requests
import re

import handlers as func

def fanTempMeasure(ipmiHost,valueInsertList,timeStamp):
	measurements = []

	hostname = ipmiHost.hostname
	username = ipmiHost.username
	password = ipmiHost.password

	output = func.ipmiTool(hostname,username,password)

	for line in output:
		line = line.split("|")
		for idx,value in enumerate(line):
			# print(value.strip())
			value = re.findall(r'^(\d*\.?\d*) ',value.strip())
			if value:
				device = line[idx-1].strip()
				value = value[0]
				measurements.append((device,value))
				pass

	for device,value in measurements:
		# print(device,value)
		device = device.replace(" ", "")
		value = value.replace(" ", "")
		if "fan" in device.lower():
			item = "fan_rpm"
		else:
			item = "temperature"

		data_fanTemp = [hostname,device,item,value]
		valueInsertList.append(func.getPostData(data_fanTemp,timeStamp))
	pass
	return valueInsertList


