#!/usr/bin/env bash

PROJECT_NAME=$1

# Grunt + Less + JS Shit
sudo npm install --unsafe-perm

source /home/vagrant/.bashrc
source `which virtualenvwrapper.sh`

rmvirtualenv ${PROJECT_NAME}
PYTHON3_PATH=`which python3.3`
mkvirtualenv ${PROJECT_NAME} -p ${PYTHON3_PATH}
workon ${PROJECT_NAME}
pip install -r ${PROJECT_NAME}/requirements.txt

DB_NAME=${PROJECT_NAME}
VIRTUALENV_NAME=${PROJECT_NAME}

PROJECT_DIR=/home/vagrant/${PROJECT_NAME}
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/${PROJECT_NAME}

cd ${PROJECT_DIR}

# Inspired by 2scoops and Jacob's slides:
# http://www.slideshare.net/jacobian/the-best-and-worst-of-django
workon ${PROJECT_NAME}
echo "export DJANGO_SETTINGS_MODULE=tecnocial.settings.development" >> /home/vagrant/.virtualenvs/${PROJECT_NAME}/bin/postactivate
echo "unset DJANGO_SETTINGS_MODULE" >> /home/vagrant/.virtualenvs/${PROJECT_NAME}/bin/postdeactivate
add2virtualenv /home/vagrant/${PROJECT_NAME}/src
