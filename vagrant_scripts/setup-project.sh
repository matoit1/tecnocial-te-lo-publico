#!/bin/bash

PROJECT_NAME=$1

source /home/vagrant/.bashrc
source /usr/local/bin/virtualenvwrapper.sh

PYTHON3_PATH=`which python3.3`
mkvirtualenv ${PROJECT_NAME} -p ${PYTHON3_PATH}

pip install -r ${PROJECT_NAME}/requirements.txt

DB_NAME=${PROJECT_NAME}
VIRTUALENV_NAME=${PROJECT_NAME}

PROJECT_DIR=/home/vagrant/${PROJECT_NAME}
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/${PROJECT_NAME}

cd ${PROJECT_DIR}

# Grunt + Less + JS Shit
sudo npm install --unsafe-perm