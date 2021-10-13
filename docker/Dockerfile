FROM library/ros:melodic-robot-bionic

# Create some directories within the Docker image that we can map to 
# the host machine's file system. Using Docker volumes, the container 
# and your host machine will then be able to share the *exact same files*!
ARG INSTALL="/scratch"
ARG SCRIPTS="/scripts"
ARG WS="/ws"
ARG SRC="${WS}/src"
RUN mkdir -p ${INSTALL} ${SCRIPTS}

# Install dependencies. This will copy "install_deps.sh" into the container,
# make it executable, and run it.
WORKDIR ${INSTALL}
RUN gpg --keyserver keyserver.ubuntu.com --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
COPY install_deps.sh ${INSTALL}
RUN chmod u+x install_deps.sh && ./install_deps.sh

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

WORKDIR ${WS}
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
