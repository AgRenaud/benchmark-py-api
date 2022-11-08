# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/focal64"
  config.ssh.insert_key = false

  config.vm.network "forwarded_port", guest: 80, host: 8088

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

  # config.vm.provider "hyperv" do |h|
  #   h.memory = 2048
  #   h.cpus = 2
  # end

  # applications = [
  #   'fastapi-gunicorn',
  #   'flask-gunicorn',
  #   'flask-mod-wsgi',
  #   'veterinary-clinic',
  # ]

  # for application in applications do
  #   config.vm.synced_folder './' + application, '/home/vagrant/' + application, type: "rsync", rsync__exclude: ["__pycache__", ".venv"]
  # end

  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yml"
  end

  # config.vm.provision "shell", inline: "apt-get update && apt-get upgrade -y", privileged: true, preserve_order: true
  # config.vm.provision "shell", inline: "apt-get install -y python3-distutils python3-apt cmake", privileged: true, preserve_order: true
  # config.vm.provision "shell", path: "./build/install-python.sh", preserve_order: true, privileged: false
  # config.vm.provision "shell", inline: ". ~/.bashrc && pyenv install 3.10.4", preserve_order: true, privileged: false
end