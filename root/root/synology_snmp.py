################################
#  - Ben Dews
#  - bendews.com
#  - 30/12/2016
#  - Script to get Synology SNMP statistics and insert to InfluxDB
################################
import subprocess
import requests
import re

import handlers as func

def sizeInGB(totalSize,allocSize):
	result = (totalSize*allocSize)/1024/1024/1024
	result = "%.4f" % result
	return result
	pass

def diskUsage(synHost,valueInsertList,timeStamp):
	storageInfoOID = ".1.3.6.1.2.1.25.2.3.1"
	storageLabelOID = storageInfoOID+".3"
	storageAllocOID = storageInfoOID+".4"
	storageTotalOID = storageInfoOID+".5"
	storageUsedOID = storageInfoOID+".6"
	disks = []
	allocationSize = []
	storageSize = []
	storageUsed = []


	hostname = synHost.hostname
	snmpCommunity = synHost.snmpCommunity
	snmpVersion = synHost.snmpVersion
	volumeList = synHost.volumeList

	output = func.snmpWalk(hostname,snmpCommunity,snmpVersion,storageInfoOID)

	for line in output:
		# Storage Label
		if ".1.3.6.1.2.1.25.2.3.1.3" in line:
			result = re.findall(r'\: (.*)',line)
			disks.append(str(result[0]))
			pass
		# Allocation Size
		if ".1.3.6.1.2.1.25.2.3.1.4" in line:
			result = re.findall(r'\: (\d*)',line)
			allocationSize.append(int(result[0]))
			pass
		# Storage total size
		if ".1.3.6.1.2.1.25.2.3.1.5" in line:
			result = re.findall(r'\: (\d*)',line)
			storageSize.append(int(result[0]))
			pass
		# Storage used
		if ".1.3.6.1.2.1.25.2.3.1.6" in line:
			result = re.findall(r'\: (\d*)',line)
			storageUsed.append(int(result[0]))
			pass
		pass

	for disk,allocSize,storSize,storUsed in zip(disks,allocationSize,storageSize,storageUsed):
		totalInTB = sizeInGB(storSize,allocSize)
		usedInTB = sizeInGB(storUsed,allocSize)
		for volume in volumeList:
			if volume in disk:
				data_totalInTB = [hostname,volume,"total_storage",totalInTB]
				valueInsertList.append(func.getPostData(data_totalInTB,timeStamp))
				data_usedInTB = [hostname,volume,"used_storage",usedInTB]
				valueInsertList.append(func.getPostData(data_usedInTB,timeStamp))
				pass
			pass
	pass
	return valueInsertList

def diskTemp(synHost,valueInsertList,timeStamp):
	diskInfoOID = ".1.3.6.1.4.1.6574.2.1.1"
	diskLabelOID = diskInfoOID+".2"
	diskTempOID = diskInfoOID+".6"
	disks = []
	temps = []


	hostname = synHost.hostname
	snmpCommunity = synHost.snmpCommunity
	snmpVersion = synHost.snmpVersion
	volumeList = synHost.volumeList

	output = func.snmpWalk(hostname,snmpCommunity,snmpVersion,diskInfoOID)

	for line in output:
		if diskLabelOID in line:
			result = re.findall(r'\"(.*)\"',line)
			disks.append(result[0])
			pass
		if diskTempOID in line:
			result = re.findall(r'\: (\d*)',line)
			temps.append(result[0])
			pass
		pass
	for disk,temp in zip(disks,temps):
		data_diskTemp = [hostname,disk,"temperature",temp]
		valueInsertList.append(func.getPostData(data_diskTemp,timeStamp))
	pass
	return valueInsertList
