#! /bin/bash

# Install packages that we need to run the rest of the project. These will all be installed in the Docker image.

# Stop the execution of this script if there's an error.
# Differs from default behavior; by default, it would keep going if there were errors.
set -e

# Install the following packages.
# The interesting one here is ninja-build, which is the build system CMR uses.
# For more information: https://ninja-build.org/

APT_PACKAGES=(\
    curl
    python3-pip \
    git \
    vim \
    ninja-build \
    wget \
    x11-apps)

apt-get update
apt-get install -y "${APT_PACKAGES[@]}"

# Install GOSU

curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.11/gosu-$(dpkg --print-architecture)"
curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.11/gosu-$(dpkg --print-architecture).asc"
gpg --verify /usr/local/bin/gosu.asc
rm /usr/local/bin/gosu.asc
chmod +x /usr/local/bin/gosu

# Install Python packages.

pip3 install docker click

# Install ROS.
# This follows the instructions from the setup article here: http://wiki.ros.org/melodic/Installation/Ubuntu

echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -

apt-get update
apt-get install -y ros-melodic-desktop
apt-get install -y python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential
apt-get install python-rosdep
rosdep update

# Make sure we can access ROS stuff in our PATH
mkdir -p /home/cmr
echo "source /opt/ros/melodic/setup.bash" >> /home/cmr/.bashrc
source /home/cmr/.bashrc
