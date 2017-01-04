# EasyInflux

[![Docker pull](https://img.shields.io/docker/pulls/dewso/easyinflux.svg)](https://hub.docker.com/r/dewso/easyinflux/) 
[![Github issues](https://img.shields.io/github/issues/bendews/EasyInflux-Docker.svg)](https://github.com/bendews/EasyInflux-Docker/issues) [![License](https://img.shields.io/github/license/bendews/EasyInflux-Docker.svg)](https://github.com/bendews/EasyInflux-Docker/blob/master/LICENSE)

A [Docker](https://www.docker.com) container that simplifies the collection of many common SNMP and IPMI data points to insert into InfluxDB. 

Initial inspiration drawn from the work done by [dencur](https://www.reddit.com/u/dencur) in [this blog post](https://denlab.io/setup-a-wicked-grafana-dashboard-to-monitor-practically-anything/)

##### Preview of supported stats

![Grafana Preview with EasyInflux stats](https://raw.githubusercontent.com/bendews/EasyInflux-Docker/master/Preview.gif)

## Getting started
EasyInflux is... easy! 
All you need:
* Configuration file
* VMWare SNMP MIB files from [VMWare KB 1013445](https://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1013445) (Only if monitoring ESXi hosts)


```
docker run -d --name easy-influx \
-v [PATH TO CONFIG FILE]:/config/config.yaml:ro \
-v [PATH TO MIB FOLDER]:/usr/share/snmp/mibs:ro \
dewso/easyinflux
```



## Configuration
A sample configuration file is located at `root/sampleConfig.yaml`.
Please view the sample configuration file to get a better understanding of its options.
Option descriptions are as follows:

##### REQUIRED - influxdb
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|hostname       |The hostname (or IP address) of the influxDB Server                                                                 |
|port           |The API port of the influxDB server (usually 8086)                                                                  |
|database       |The database for EasyInflux to write data to (a new database is recommended)                                        |
|insert_interval|The time interval in seconds that values are collected and sent to InfluxDB (a value of 30 or higher is recommended)|
##### Optional - esxi_hosts
|Key            |Description                                                                                                         |
:---------------|:-------------------------------------------------------------------------------------------------------------------|
|hostname       |The hostname (or IP address) of the ESXi Server                                                                     |
|snmp_community |The SNMP community string for this host                                                                             |
|snmp_version   |The SNMP version for this host ("1" or "2c" supported at this time)                                                 |
##### Optional - synology_hosts
|Key            |Description                                                                                                         |
:---------------|:-------------------------------------------------------------------------------------------------------------------|
|hostname       |The hostname (or IP address) of the Synology Server                                                                 |
|snmp_community |The SNMP community string for this host                                                                             |
|snmp_version   |The SNMP version for this host ("1" or "2c" supported at this time)                                                 |
|volumes        |The volumes on the Synology host to be reported ("volume1", "volume2" etc.)                                         |
##### Optional - ipmi_hosts
|Key            |Description                                                                                                         |
:---------------|:-------------------------------------------------------------------------------------------------------------------|
|hostname       |The hostname (or IP address) of the IPMI supported device                                                           |
|ipmi_username  |The IPMI username for this host                                                                                     |
|ipmi_password  |The IPMI password for this host                                                                                     |
##### Optional - ups_hosts
|Key            |Description                                                                                                         |
:---------------|:-------------------------------------------------------------------------------------------------------------------|
|hostname       |The hostname (or IP address) of the UPS SNMP interface                                                              |
|snmp_community |The SNMP community string for this host                                                                             |
|snmp_version   |The SNMP version for this host ("1" or "2c" supported at this time)                                                 |

Note that **ALL** values should be string escaped (I.E, be within "quotation marks")

## [License]()