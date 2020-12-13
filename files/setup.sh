#!/bin/bash

sudo apt update
sudo apt upgrade -y
sudo apt update

# Just enough x windows to correctly run pygame with touch input
#sudo apt-get install --no-install-recommends xorg

# Install pip
sudo apt-get install -y python-pip python3-pip
sudo apt-get install -y --fix-missing python3-pip
sudo apt-get install -y --fix-missing python3-picamera
sudo apt-get install -y --fix-missing python3-pygame
sudo apt-get install -y --fix-missing python3-opencv
sudo apt --fix-broken -y install

# Create run script
(
cat <<'END_OF_CONTENT'
#!/bin/bash
sudo python3 /home/pi/code/pi-nv/src/camera-ui/pg-picam-ui.py
END_OF_CONTENT
) > ~/run.sh
chmod +x ~/run.sh
