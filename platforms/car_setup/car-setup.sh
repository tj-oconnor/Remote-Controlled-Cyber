#!/bin/bash

echo "[+] Beginning RCCTF installation..."

if [ $(whoami) != "root" ]; then
    echo "Please run as root: sudo $0"
    exit 1
fi

ssid=$1

if [ -z $ssid ]; then
    echo "Usage: $0 <ssid>"
    exit 1
fi

echo "[+] Installing package depencies..."

sudo apt update
sudo apt -y upgrade
sudo apt -y autoremove
sudo apt -y install \
    docker.io \
    python3 \
    python3-pip \
    git \
    wget \
    curl \
    i2c-tools \
    libi2c-dev

echo "[+] Adding user pi to docker group..."
sudo usermod -aG docker pi

echo "[+] Checking i2c availability..."
if [ ! -c "/dev/i2c-1" ]; then
    echo "[+] i2c is not enabled.  Enabling..."
    echo -e "i2c-dev\ni2c-bcm2708" >> /etc/modules
    echo -e "dtparam=i2c_arm=on\ndtparam=i2c1=on" >> /boot/config.txt
else
    echo "[+] i2c already enabled.  Skipping..."
fi

pushd admin-app
./install.sh
popd

echo "Installing RaspAP"
wget -O raspap-install.sh https://install.raspap.com

chmod +x raspap-install.sh

./raspap-install.sh -y -o 0 -a 0

echo "Changing SSID to $ssid"
sed -i "s/raspi-webgui/$ssid/g" /etc/hostapd/hostapd.conf
sed -i 's/wpa=2/wpa=0/g' /etc/hostapd/hostapd.conf

echo "Changing lighttpd server port to 8080"
sed -i 's/= 80/= 8080/g' /etc/lighttpd/lighttpd.conf

echo "[+] Setup complete.  Rebooting in 10 seconds..."
sleep 10
reboot
