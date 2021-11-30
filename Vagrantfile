# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "generic/ubuntu1804"
  config.vm.define "pathfinder"
  
  # Disable the default because we want to rename it.
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", "/Pathfinder"

  # Enable X11 forwarding
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true 

  # For each provider, we can set settings like the amount of memory our machine has.

  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "4096"
  end

  config.vm.provider "vmware_fusion" do |vf|
      vf.memory = "4096"
  end

  # This will run the following shell script ONCE, when the machine is first created.
  config.vm.provision "shell", inline: <<-SHELL

    # Install some tools we need to set up our development environment, like git and Python 3.
    apt-get update
    apt-get install -y git apt-transport-https ca-certificates curl gnupg lsb-release python3 python3-pip

    # Install Xpra for X Forwarding (lets us see GUI's within the virtual machine)
    apt-get install ca-certificates
    wget -q https://xpra.org/gpg.asc -O- | sudo apt-key add -
    cd /etc/apt/sources.list.d; wget https://xpra.org/repos/bionic/xpra.list
    apt-get update
    apt-get install -y xpra x11-apps

    # Install ROS
    echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -

    apt-get update
    apt-get install -y ros-melodic-desktop
    apt-get install -y python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential
    apt-get install python-rosdep
    echo "source /opt/ros/melodic/setup.bash" >> /home/vagrant/.bashrc
    source /home/vagrant/.bashrc
  SHELL

  config.vm.provision "docker"

  # Sync VM's time with host machine's. Runs each time the machine is started.
  config.vm.provision :shell, :inline => "sudo rm /etc/localtime && sudo ln -s /usr/share/zoneinfo/Europe/Paris /etc/localtime", run: "always"

  # Start the Xpra server. Runs each time the machine is started.
  config.vm.provision :shell, :inline => 'xpra start', run: "always", privileged: false

end