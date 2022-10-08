# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "bento/ubuntu-20.04"
  config.ssh.insert_key = false

  config.vm.network "forwarded_port", guest: 80, host: 8088

  config.vm.provider "virtualbox" do |vb|
    vb.name = "python-benchmark-api"
    vb.gui = false
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.synced_folder '.', '/vagrant'
end