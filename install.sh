#!/bin/bash

apt-get update
apt-get -y upgrade
apt-get -y dist-upgrade
apt-get -y install build-essential

apt-get -y install libssl-dev
apt-get -y install libffi-dev
apt-get -y install python-dev

apt-get -y install nginx

nginx -s stop

apt-get -y install python-setuptools

easy_install pip

apt-get install -y python-mysqldb

git clone https://github.com/c475/yt.git /srv/

rm -f /etc/nginx/sites-available/default
rm -f /etc/nginx/sites-enabled/default

cp /srv/config/nginx/* /etc/nginx/sites-available
cp /srv/config/nginx/* /etc/nginx/sites-enabled

pip install -r /srv/requirements.txt
pip install crossbar[tls,msgpack,manhole,system]

python /srv/manage.py collectstatic --noinput

cp /srv/config/services/* /lib/systemd/system/

sudo apt-get install -y fail2ban
sudo cp /srv/config/misc/jail.local /etc/fail2ban/
sudo service fail2ban restart

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/mediacenter.key -out /etc/ssl/certs/mediacenter.crt
sudo chown -R www-data /etc/ssl/private

python /srv/scripts/restart.py
