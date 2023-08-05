# vim:set ft=dockerfile:
FROM birdhouse/bird-base:latest
MAINTAINER ${maintainer}

LABEL Description="${description}" Vendor="${vendor}" Version="${version}"

# Configure hostname and ports for services
ENV HTTP_PORT ${http_port}
ENV HTTPS_PORT ${https_port}
ENV OUTPUT_PORT ${output_port}
ENV HOSTNAME ${hostname}

# Set current home
ENV HOME /root

# Copy application sources
COPY . /opt/birdhouse/src/${app}

# cd into application
WORKDIR /opt/birdhouse/src/${app}

# Provide custom.cfg with settings for docker image
RUN printf "[buildout]\nextends=profiles/docker.cfg" > custom.cfg

# Install system dependencies
RUN bash bootstrap.sh -i && bash requirements.sh

# Set conda enviroment
ENV ANACONDA_HOME /opt/conda
ENV CONDA_ENVS_DIR /opt/conda/envs

# Run install and fix permissions
RUN make clean install && chmod 755 /opt/birdhouse/etc && chmod 755 /opt/birdhouse/var/run

# Volume for data, cache, logfiles, ...
VOLUME /opt/birdhouse/var/lib
VOLUME /opt/birdhouse/var/log
# Volume for configs
VOLUME /opt/birdhouse/etc

# Ports used in birdhouse
EXPOSE 9001 $HTTP_PORT $HTTPS_PORT $OUTPUT_PORT

# Start supervisor in foreground
ENV DAEMON_OPTS --nodaemon

# Start service ...
CMD ["make", "update-config", "start"]
