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
import argparse

import esx_snmp
import synology_snmp
import ups_snmp
import misc_ipmi

import host_classes as host
import handlers as func

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError


currentDirectory = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.DEBUG)
	
class influxDB():

	def __init__(self,influx_config):
		super().__init__()
		self.output = True
		self.measurementList = []
		self.influx_config = influx_config
		self.timestamp = self.get_timestamp()
		self.influx_client = InfluxDBClient(
			host=self.influx_config["hostname"],
			port=self.influx_config["port"],
			database=self.influx_config["database"]
		)

	def append_measurement(self,measurement):		
		host = str(measurement[0]).replace(" ", "")
		device = str(measurement[1]).replace(" ", "")
		item = str(measurement[2]).replace(" ", "")
		try:
			value = int(measurement[3])
		except ValueError:
			value = int(float(measurement[3]))
			pass
		self.measurementList.append({
					'measurement': item+"_TEST",
					'fields': {
						'value': value
					},
					"time": self.timestamp,
					'tags': {
						'device': device,
						'host': host
					}
				})
		pass

	# Round unix time to closest interval period
	def get_timestamp(self):
		unixTime = time.time()
		secondsToRound = float(self.influx_config["insert_interval"])
		return int(round(unixTime / secondsToRound) * secondsToRound)
		pass

	def write_data(self):
		print(self.measurementList)
		try:
			self.influx_client.write_points(self.measurementList,time_precision="s")
		except (InfluxDBClientError, ConnectionError, InfluxDBServerError) as e:
			if hasattr(e, 'code') and e.code == 404:
				self.influx_client.create_database(self.influx_config["database"])
				self.influx_client.write_points(self.measurementList)
				return
			print('Failed to write data to InfluxDB', 'error')
			print('ERROR: Failed To Write To InfluxDB')
			print(e)
		print('Written To Influx: {}'.format(self.measurementList), 'debug')


class easyInfluxCollector(object):

	def __init__(self):
		super().__init__()

		self.config = configManager()

		self.INFLUX_CONFIG = self.config.INFLUX_CONFIG
		self.INSERT_INTERVAL = float(self.INFLUX_CONFIG["insert_interval"])
		self.ESXI_HOSTS = self.config.ESXI_HOSTS
		self.IPMI_HOSTS = self.config.IPMI_HOSTS
		self.SYNOLOGY_HOSTS = self.config.SYNOLOGY_HOSTS
		self.UPS_HOSTS = self.config.UPS_HOSTS

	def get_esx_stats(self):
		for hostData in self.ESXI_HOSTS:
			esxHost = host.EsxHost(hostData["hostname"],hostData["snmp_community"],hostData["snmp_version"])
			esx_snmp.procLoad(esxHost,self.influx)
			esx_snmp.VMList(esxHost,self.influx)
		pass

	def get_ipmi_stats(self):
		for hostData in self.IPMI_HOSTS:
			ipmiHost = host.IpmiHost(hostData["hostname"],hostData["ipmi_username"],hostData["ipmi_password"])
			misc_ipmi.fanTempMeasure(ipmiHost,self.influx)
		pass
	def get_synology_stats(self):
		for hostData in self.SYNOLOGY_HOSTS:
			volumes = hostData.get('volumes',[])
			synHost = host.SynologyHost(hostData["hostname"],hostData["snmp_community"],hostData["snmp_version"],volumes)
			synology_snmp.diskUsage(synHost,self.influx)
			synology_snmp.diskTemp(synHost,self.influx)
		pass
	def get_ups_stats(self):
		for hostData in self.UPS_HOSTS:
			upsHost = host.UpsHost(hostData["hostname"],hostData["snmp_community"],hostData["snmp_version"])
			ups_snmp.upsPower(upsHost,self.influx)
		pass

	def run(self):
		print('Starting Data Collection Loop \n ')
		while True:
			self.influx = influxDB(self.INFLUX_CONFIG)

			logging.debug("Gathering statistics every "+str(self.INSERT_INTERVAL)+" seconds")
			logging.debug("Actual Time:"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
			logging.debug("Timestamp for data:"+datetime.datetime.fromtimestamp(self.influx.timestamp).strftime('%Y-%m-%d %H:%M:%S'))

			self.get_esx_stats()
			self.get_ipmi_stats()
			self.get_synology_stats()
			self.get_ups_stats()

			self.influx.write_data()

			# Delay data collection loop to match interval period
			timeToSleep = self.INSERT_INTERVAL - ((time.time() - self.influx.timestamp) % self.INSERT_INTERVAL)
			logging.info("Statistics gathered, sleeping for "+str(timeToSleep)+" seconds")
			time.sleep(timeToSleep)
			pass

class configManager():

	def __init__(self):
		print('Loading Configuration File')
		config_file = currentDirectory+"/../config/config.yaml"
		with open(config_file, 'r') as stream:
			try:
				self.config = yaml.load(stream)
			except yaml.YAMLError as err:
				logging.error(err)
				exit(1)
		self._load_config_values()

	def _load_config_values(self):
		try:
			self.INFLUX_CONFIG = self.config["influxdb"]
			self.ESXI_HOSTS = self.config.get('esxi_hosts',[])
			self.IPMI_HOSTS = self.config.get('ipmi_hosts',[])
			self.SYNOLOGY_HOSTS = self.config.get('synology_hosts',[])
			self.UPS_HOSTS = self.config.get('ups_hosts',[])
		except (KeyError,TypeError,NameError) as err:
			logging.error("Please check your configuration file! An error occurred whilst parsing:",err)
			exit(1)

def main():
	parser = argparse.ArgumentParser(description="Easy to use solution for inputting common data metrics into InfluxDB")
	# parser.add_argument('--config', default='config.ini', dest='config', help='Specify a custom location for the config file')
	args = parser.parse_args()
	collector = easyInfluxCollector()
	collector.run()

if __name__ == '__main__':
	main()