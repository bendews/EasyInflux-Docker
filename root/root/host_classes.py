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
		Host.__init__(self, hostname)
		self.snmpCommunity = snmpCommunity
		self.snmpVersion = snmpVersion
	def snmpCommunity(self):
		print(self.snmpCommunity)
	def snmpVersion(self):
		print(self.snmpVersion)

# Base IPMI Class
class IpmiHost(Host):
	# Init Class Object
	def __init__(self, hostname, username, password):
		Host.__init__(self, hostname)
		self.username = username
		self.password = password
	def username(self):
		print(self.username)
	def password(self):
		print(self.password)

# ESX Host Class
class EsxHost(SnmpHost):
	# Init Class Object
	def __init__(self, hostname, snmpCommunity, snmpVersion):
		SnmpHost.__init__(self, hostname, snmpCommunity,snmpVersion)

# UPS Host Class
class UpsHost(SnmpHost):
	# Init Class Object
	def __init__(self, hostname, snmpCommunity, snmpVersion):
		SnmpHost.__init__(self, hostname, snmpCommunity,snmpVersion)

# Synology Host Class
class SynologyHost:
	# Init Class Object
	def __init__(self, hostname, snmpCommunity, snmpVersion, volumeList):
		SnmpHost.__init__(self, hostname, snmpCommunity,snmpVersion)
		self.volumeList = volumeList
	def volumeList(self):
		print(self.volumeList)