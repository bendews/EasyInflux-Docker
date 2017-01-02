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
	print(data)
	requests.post(url, data=data,headers={'Content-Type': 'application/octet-stream'},timeout = 3)
	pass

def snmpWalk(hostData,oid):
	SNMP_SERVER = hostData['hostname']
	SNMP_COMMUNITY = hostData['community']

	p = subprocess.run(["snmpwalk", "-O", "fn", "-v", "1", "-c", SNMP_COMMUNITY, SNMP_SERVER, oid], stdout=subprocess.PIPE)
	output = p.stdout.decode('utf8').splitlines()
	return output
	pass

def upsPower(influxData,hostData,timeStamp):
	output = snmpWalk(hostData,"1.3.6.1.2.1.33.1")

	for line in output:
		if "2.33.1.4.4.1.4.1" in line:
			result = re.findall(r'\: (\d*)',line)
			upsPower = str(result[0])
			data_upsPower = [hostData['hostname'],"ActivePower","ups_power",upsPower]
			writeData(influxData,data_upsPower,timeStamp)
		pass
	pass
