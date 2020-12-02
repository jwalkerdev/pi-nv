#!/bin/bash

sudo apt update
sudo apt upgrade -y
#sudo apt-get upgrade -y
sudo apt-get install -y git
# Install pip
sudo apt-get install -y python-pip python3-pip

# Install RPi.GPIO
sudo apt-get install -y python-dev python-rpi.gpio python3-dev python3-rpi.gpio
# Install gpiozero for the tools and libs
sudo apt-get install -y python-gpiozero python3-gpiozero

mkdir -p ~/code
cd ~/code
git clone https://github.com/jwalkerdev/pi-nv.git
cd pi-nv

sudo apt-get install -y --fix-missing python-pip
sudo apt-get install -y --fix-missing python-picamera
sudo apt-get install -y --fix-missing python-pygame
sudo apt-get install -y --fix-missing python-opencv
sudo apt-get install -y --fix-missing python3-pip
sudo apt-get install -y --fix-missing python3-picamera
sudo apt-get install -y --fix-missing python3-pygame
sudo apt-get install -y --fix-missing python3-opencv

sudo apt-get install -y --fix-missing omxplayer vlc
sudo apt --fix-broken -y install
sudo apt-get install -y --fix-missing omxplayer vlc
