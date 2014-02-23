#!/usr/bin/env bash

PROJECT_NAME=$1

apt-get update
sudo apt-get install -y python-software-properties
add-apt-repository -y ppa:chris-lea/node.js
apt-get update

# Utilities
apt-get install -y vim python g++ make git

# Node + NPM
apt-get install -y nodejs

# Python stuff
apt-get install -y build-essential python python-dev python-setuptools python-pip

# Dependencies for image processing with PIL
apt-get install -y libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev

# MySQL Shit
echo mysql-server mysql-server/root_password password tecnocial | debconf-set-selections
echo mysql-server mysql-server/root_password_again password tecnocial | sudo debconf-set-selections
apt-get install -y mysql-server mysql-client mysql-common

# Dependencies for Python 3
apt-get install -y libsqlite3-dev sqlite3 bzip2 libbz2-dev
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get -y install python3.3

pip install virtualenv virtualenvwrapper

printf "\n" >> /home/vagrant/.bashrc

echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
echo "export PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc