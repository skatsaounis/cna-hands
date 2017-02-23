# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.
  config.vm.box_version = "14.04"

  # Keep insecure keypair
  config.ssh.insert_key = false

  # Delete proxy configuration after done
  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http     = "http://10.124.32.12:80"
    config.proxy.https    = "http://10.124.32.12:80"
    config.proxy.no_proxy = "localhost,127.0.0.1,0.0.0.0"
  end

  config.vm.define "virtualbox" do |vbox|
    vbox.vm.provider "virtualbox" do |v|
      v.memory = 2048
      v.cpus = 2
    end

    vbox.vm.box = "ubuntu/trusty64"

    vbox.vm.network "forwarded_port", guest: 80, host: 8080

    # Delete proxy configuration after done
    vbox.vm.provision "shell", privileged: true, inline: <<-SHELL
      DOCKER_SERVICE_D=/etc/systemd/system/docker.service.d
      DOCKER_PROXY_CONF=${DOCKER_SERVICE_D}/http_proxy.conf
      mkdir -p $DOCKER_SERVICE_D
      echo "[Service]" > $DOCKER_PROXY_CONF
      echo 'Environment="HTTP_PROXY=http://10.124.32.12:80"' >> $DOCKER_PROXY_CONF
      echo 'Environment="HTTPS_PROXY=http://10.124.32.12:80"' >> $DOCKER_PROXY_CONF
      echo 'Environment="NO_PROXY=localhost,127.0.0.0/8,0.0.0.0"' >> $DOCKER_PROXY_CONF
    SHELL

    # Install latest docker
    # Yes this is implicit
    vbox.vm.provision :docker #,
 # Fetching images this way works w/o company proxy
 # TODO: test @ home
 #     images: [
 #       "kobolog/gorb",
 #       "golang:latest",
 #       "python:2.7",
 #       "python:3.4"
 #     ]

    vbox.vm.provision "shell", privileged: true, inline: <<-SHELL
      service docker restart
      sleep 10s
      # Install GORB
      docker pull kobolog/gorb
      docker pull golang:latest
      docker pull python:2.7

      add-apt-repository ppa:webupd8team/atom
      apt update

      # Install docker-compose
      curl -L curl -L https://github.com/docker/compose/releases/download/1.9.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
      chmod +x /usr/local/bin/docker-compose

      # Install go
      wget https://storage.googleapis.com/golang/go1.7.1.linux-amd64.tar.gz -O /tmp/go.tar.gz
      tar -C "/usr/local/" -xzf /tmp/go.tar.gz
      {
        echo '# GoLang'
        echo 'export GOROOT=/usr/local/go'
        echo 'export PATH=$PATH:$GOROOT/bin'
        echo 'export DOCKER_API_VERSION="1.24"'
      } >> "/etc/profile"
      mkdir -p /usr/local/go/{src,pkg,bin}
      echo -e "\nGo 1.7.1 was installed.\n"
      rm -f /tmp/go.tar.gz

      # Install needed packages
      apt install -y git python-pip
      apt install -y inotify-tools pv
      # Install ipvsadm
      apt install -y ipvsadm

      # install xfce + dev tools
      apt install xfce4 terminator vim atom tmux

      # Install docker SDK for python
      pip install docker

      # Add user to docker group
      usermod -a -G docker vagrant
    SHELL

    vbox.vm.provision "shell", privileged: false, inline: <<-SHELL
      # Setup go workspace, see https://golang.org/doc/code.html
      mkdir -p $HOME/go/{src,pkg,bin}
      {
        echo 'export GOPATH=$HOME/go'
        echo 'export PATH=$PATH:$GOPATH/bin'
      } >> "$HOME/.bashrc"
      export GOPATH=$HOME/go
      export PATH=$PATH:$GOPATH/bin

      # Install godep, see https://github.com/tools/godep
      echo "Installing godep"
      strace -f -e trace=network go get github.com/tools/godep 2>&1 | pv -i 0.05 > /dev/null
      # Install docker SDK for go

      echo "Installing docker SDK for golang..."
      mkdir -p $GOPATH/src/github.com/docker
      pushd $GOPATH/src/github.com/docker
      git clone https://github.com/docker/docker/
      rm -rm $GOPATH/src/github.com/docker/docker/vendor
      git clone https://github.com/docker/go-connections
      popd

      echo "Installig dependencies..."
      strace -f -e trace=network go get github.com/gorilla/mux 2>&1 | pv -i 0.05 > /dev/null
      strace -f -e trace=network go get github.com/Sirupsen/logrus 2>&1 | pv -i 0.05 > /dev/null
      strace -f -e trace=network go get github.com/docker.go-units 2>&1 | pv -i 0.05 > /dev/null

    SHELL
  end
end
