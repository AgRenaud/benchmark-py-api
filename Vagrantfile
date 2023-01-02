# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/focal64"
  config.ssh.insert_key = false
  config.vm.network :private_network, ip: "192.168.56.20"


  config.vm.provider "virtualbox" do |vb|
    vb.name = "python-benchmark-api"
    vb.memory = 2048
    vb.cpus = 2
    vb.gui = false
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
    vb.customize ["modifyvm", :id, "--usb", "on"]
    vb.customize ["modifyvm", :id, "--usbehci", "off"]
    vb.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
  end

  config.vm.provision "ansible" do |ansible|
    ansible.verbose = true
    ansible.playbook = "playbook.yml"
  end
end