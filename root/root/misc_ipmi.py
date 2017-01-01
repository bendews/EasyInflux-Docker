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


def ipmiTool(hostData):
	IPMI_SERVER = hostData['hostname']
	IPMI_USERNAME = hostData['username']
	IPMI_PASSWORD = hostData['password']
	
	p = subprocess.run(["ipmitool", "-H", IPMI_SERVER, "-U", IPMI_USERNAME, "-P", IPMI_PASSWORD, "-I", "lanplus", "sdr", "list", "full"], stdout=subprocess.PIPE)
	output = p.stdout.decode('utf8').splitlines()

	return output
	pass

def fanTempMeasure(influxData,hostData,timeStamp):
	measurements = []

	output = ipmiTool(hostData)

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

		data_fanTemp = [hostData['hostname'],device,item,value]
		writeData(influxData,data_fanTemp,timeStamp)
	pass


