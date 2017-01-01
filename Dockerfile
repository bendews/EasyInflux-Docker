FROM docker/ubuntu
MAINTAINER Ben Dews, dewso

# package version
# ENV PLEX_INSTALL="https://plex.tv/downloads/latest/1?channel=8&build=linux-ubuntu-x86_64&distro=ubuntu"

# global environment settings
# ENV DEBIAN_FRONTEND="noninteractive"
# ENV HOME="/config"
# ENV PLEX_DOWNLOAD="https://downloads.plex.tv/plex-media-server"

# install packages
# RUN \
#  apt-get update && \
#  apt-get install -y \
# 	ipmitool \
# 	python3 \
# 	snmp &&

RUN apt-get update
RUN apt-get install -qy ipmitool
RUN apt-get install -qy snmp
RUN apt-get install -qy python3
RUN apt-get install -qy python3-pip
RUN pip3 install PyYAML==3.12
RUN pip3 install requests==2.12.4

# install plex
 # curl -o \
	# /tmp/plexmediaserver.deb -L \
	# "${PLEX_INSTALL}" && \
 # dpkg -i /tmp/plexmediaserver.deb && \

# cleanup
RUN apt-get clean
RUN rm -rf
RUN /tmp/*
RUN /var/lib/apt/lists/*
RUN /var/tmp

# add local files
COPY root/ /

# ports and volumes
# EXPOSE 32400 32400/udp 32469 32469/udp 5353/udp 1900/udp
VOLUME /config /mibs

