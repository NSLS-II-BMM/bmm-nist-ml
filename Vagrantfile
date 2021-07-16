Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.box_check_update = true

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "4096"
    # vb.cpus = 4
  end

  # it may be helpful to run a browser inside the VM
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true

  # forward the mongodb port to the host
  config.vm.network "forwarded_port", guest: 27017, host: 27017, host_ip: "localhost"

  # forward the port for interactive API documentation
  config.vm.network "forwarded_port", guest: 60610, host: 60610, host_ip: "localhost"

  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt full-upgrade
    # install X11 for firefox
    apt install -y firefox xserver-xorg-core x11-utils

    apt install -y httpie redis-server

    # install mongodb
    # note: change the mongodb bindIP in /etc/mongod.conf to 0.0.0.0 to allow connections from the host
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
    apt update
    apt install -y mongodb-org
    systemctl start mongod
    systemctl enable mongod

    # install miniconda3
    wget -P /tmp https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p /home/vagrant/miniconda3
    rm /tmp/Miniconda3-latest-Linux-x86_64.sh

    /home/vagrant/miniconda3/bin/conda init --system
    /home/vagrant/miniconda3/bin/conda update conda -y

    /home/vagrant/miniconda3/bin/conda create -y -n bluesky_queueserver python=3.8
    /home/vagrant/miniconda3/envs/bluesky_queueserver/bin/pip install uvicorn
    /home/vagrant/miniconda3/bin/conda install zeromq -n bluesky_queueserver
    # use tiled as well
    /home/vagrant/miniconda3/envs/bluesky_queueserver/bin/pip install tiled[complete]

    git clone https://github.com/bluesky/bluesky-queueserver.git /home/vagrant/bluesky-queueserver
    cd /home/vagrant/bluesky-queueserver
    /home/vagrant/miniconda3/envs/bluesky_queueserver/bin/pip install .
    chown -R vagrant:vagrant /home/vagrant/bluesky-queueserver

    # must change ownership for /home/vagrant/miniconda3 after creating virtual environments and installing packages
    chown -R vagrant:vagrant /home/vagrant/miniconda3

  SHELL
end
