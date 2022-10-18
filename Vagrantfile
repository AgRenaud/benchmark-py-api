# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "generic/ubuntu2004"
  config.ssh.insert_key = true

  config.vm.network "forwarded_port", guest: 80, host: 8088

  config.vm.provider "virtualbox" do |vb|
    vb.name = "python-benchmark-api"
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.provider "hyperv" do |h|
    h.name = "python-benchmark-api"
    h.memory = 2048
    h.cpus = 2
  end

  config.vm.synced_folder '.', '/home/vagrant'

  config.vm.provision "shell", inline: "apt-get update && apt-get upgrade -y", privileged: true, preserve_order: true
  config.vm.provision "shell", path: "./build/install-python.sh", privileged: false, preserve_order: true
end