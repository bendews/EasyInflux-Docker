# import subprocess
# import requests

# def getPostData(measurementData,timeStamp):
# 	host = str(measurementData[0]).replace(" ", "")
# 	device = str(measurementData[1]).replace(" ", "")
# 	item = str(measurementData[2]).replace(" ", "")
# 	value = str(measurementData[3]).replace(" ", "")

# 	data = item+",device="+device+",host="+host+" value="+value+" "+str(timeStamp)
# 	return(data)
# 	pass

# def snmpWalk(SNMP_SERVER,SNMP_COMMUNITY,SNMP_VERSION,oid):
# 	SNMP_VERSION = str(SNMP_VERSION)

# 	p = subprocess.run(["snmpwalk", "-O", "fn", "-v", SNMP_VERSION, "-c", SNMP_COMMUNITY, SNMP_SERVER, oid], stdout=subprocess.PIPE)
# 	output = p.stdout.decode('utf8').splitlines()
# 	return output
# 	pass

# def ipmiTool(hostname,username,password):
# 	IPMI_SERVER = hostname
# 	IPMI_USERNAME = username
# 	IPMI_PASSWORD = password

# 	p = subprocess.run(["ipmitool", "-H", IPMI_SERVER, "-U", IPMI_USERNAME, "-P", IPMI_PASSWORD, "-I", "lanplus", "sdr", "list", "full"], stdout=subprocess.PIPE)
# 	output = p.stdout.decode('utf8').splitlines()

# 	return output
# 	pass