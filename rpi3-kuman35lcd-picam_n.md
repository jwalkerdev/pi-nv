# 

## Install Raspbian or Raspbian Lite

Write image to SD card with Etcher / Balena Etcher.

Assuming, the SD gets mounted to /Volumes/boot on the local system (osx for me), run the following commands:
```bash
touch ssh
touch wpa_supplicant.conf
(cat <<'END_OF_FILE'
country=us
update_config=1
ctrl_interface=/var/run/wpa_supplicant
network={
 scan_ssid=1
 ssid="MyNetworkSSID"
 psk="ThePassword"
}
END_OF_FILE
) > wpa_supplicant.conf
```

## Configure the Pi

Find the raspberry pi on the network

ssh to it.
`ssh pi@ip_address`

## Change the password for the pi user
`passwd`

### General Setup
```bash
# Update apt-get and install dependencies
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
#sudo apt-get upgrade -y
sudo apt-get install -y git python3-pip python3-dev python3-rpi.gpio python3-gpiozero

# Run test commands
pinout
pinout --monochrome
# Ex. check pinout on pi 3B+
pinout -r a020d3
# Ex. check pinout on pi zero W
pinout -r 9000c1

# Install tools and libs
#sudo apt-get install -y --fix-missing python3-pip 
sudo apt-get install -y --fix-missing python3-picamera
sudo apt-get install -y --fix-missing python3-pygame
sudo apt-get install -y --fix-missing python3-opencv
# sudo apt -y --fix-broken install
# sudo apt-get install -y --fix-missing python3-pygame
# sudo apt-get install -y --fix-missing python3-opencv

# Prepare code directory for project code
mkdir -p ~/code
cd ~/code
git clone https://github.com/jwalkerdev/pi-nv.git
# Download rpi_camera_surveillance_system.py
curl -O -k https://raw.githubusercontent.com/RuiSantosdotme/Random-Nerd-Tutorials/master/Projects/rpi_camera_surveillance_system.py
```

## Install Kuman 3.5in HDMI display
### Directions from Kuman doc
#### If not using the raspbian image from the DVD, add the drivers to the PI from the DVD

#### Update /boot/config.txt
```
hdmi_drive=2
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt 480 320 60 6 0 0 0
```

#### Reboot the pi

#### Install drivers and enable LCD

```bash
# On public network, run this. Otherwise, manually copy the drivers to the pi
cd ~/code
curl -L -k -O https://www.dropbox.com/s/jrw8bnb4vswo309/LCD-show.tar.gz

# Unpack the file and set permissions
tar xzf LCD-show.tar.gz
cd LCD-show
chmod +x LCD* MPI*show
sudo ./MPI3508_480_320-show
```

## Enable the camera

Login to the pi
Run `sudo raspi-config`
Enable the camera
Reboot the pi
