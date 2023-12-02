#!/bin/bash

# installs
sudo python3 -m pip install docker
sudo python3 -m pip install flask
sudo python3 -m pip uninstall markupsafe
sudo python3 -m pip install markupsafe==2.0.1

# pull docker containers
sudo python3 service/refresh.py

# install service
sudo chmod +x /home/pi/admin-app/service/web.sh
sudo cp /home/pi/admin-app/service/web.service /etc/systemd/system/web.service
sudo systemctl enable /etc/systemd/system/web.service
sudo systemctl start web.service

