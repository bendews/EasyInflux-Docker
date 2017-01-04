FROM ubuntu:xenial
MAINTAINER Ben Dews, bendews

RUN apt-get update && \
	apt-get install -qy --no-install-recommends ipmitool && \
	apt-get install -qy --no-install-recommends snmp && \
	apt-get install -qy --no-install-recommends python3 && \
	apt-get install -qy --no-install-recommends python3-pip && \
	apt-get install -qy --no-install-recommends python3-setuptools && \
	pip3 install wheel==0.29.0 && \
	pip3 install PyYAML==3.12 && \
	pip3 install requests==2.12.4 && \

# cleanup
	apt-get clean && \
	rm -rf /tmp/* && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/tmp

# add local files
COPY root/ /

# ports and volumes
# EXPOSE 32400 32400/udp 32469 32469/udp 5353/udp 1900/udp
VOLUME ["/config","/usr/share/snmp/mibs"]

ENTRYPOINT ["/usr/bin/python3", "root/easy_influx.py"]  