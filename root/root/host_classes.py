import subprocess

# Base Class
class Host:
	# Init Class Object
	def __init__(self, hostname):
		self.hostname = hostname
	def hostname(self):
	  print(self.hostname)

# Base SNMP Class
class SnmpHost(Host):
	# Init Class Object
	def __init__(self, hostname, snmpCommunity, snmpVersion):
		super().__init__(hostname)
		self.snmpCommunity = snmpCommunity
		self.snmpVersion = str(snmpVersion)
	def snmpCommunity(self):
		print(self.snmpCommunity)
	def snmpVersion(self):
		print(self.snmpVersion)

	def snmpWalk(self,oid):
		p = subprocess.run(["snmpwalk", "-O", "fn", "-v", self.snmpVersion, "-c", self.snmpCommunity, self.hostname, oid], stdout=subprocess.PIPE)
		output = p.stdout.decode('utf8').splitlines()
		return output
	pass

# Base IPMI Class
class IpmiHost(Host):
	# Init Class Object
	def __init__(self, hostname, username, password):
		super().__init__(hostname)
		self.username = username
		self.password = password
	def username(self):
		print(self.username)
	def password(self):
		print(self.password)

	def ipmiTool(self):
		p = subprocess.run(["ipmitool", "-H", self.hostname, "-U", self.username, "-P", self.password, "-I", "lanplus", "sdr", "list", "full"], stdout=subprocess.PIPE)
		output = p.stdout.decode('utf8').splitlines()
		return output
	pass

# ESX Host Class
class EsxHost(SnmpHost):
	# Init Class Object
	def __init__(self, hostname, snmpCommunity, snmpVersion):
		super().__init__(hostname, snmpCommunity,snmpVersion)

# UPS Host Class
class UpsHost(SnmpHost):
	# Init Class Object
	def __init__(self, hostname, snmpCommunity, snmpVersion):
		super().__init__(hostname, snmpCommunity,snmpVersion)

# Synology Host Class
class SynologyHost(SnmpHost):
	# Init Class Object
	def __init__(self, hostname, snmpCommunity, snmpVersion, volumeList):
		super().__init__(hostname, snmpCommunity,snmpVersion)
		self.volumeList = volumeList
	def volumeList(self):
		print(self.volumeList)