#


nohup python3 /home/pi/code/rpi_camera_surveillance_system.py 1>/dev/null 2>&1 &
sleep 1
python3 /home/pi/code/pi-nv/camera-ui/pygame/pg-stream-ui.py
---
git -C /home/pi/code/pi-nv
python3 /home/pi/code/pi-nv/camera-ui/pygame/pg-picam-ui.py
---
mkdir /home/pi/.config/autostart
nano /home/pi/.config/autostart/pg-picam-ui.desktop
# contents of pg-picam-ui.desktop
[Desktop Entry]
Type=Application
Name=Picam-UI
Exec=/usr/bin/python3 /home/pi/code/pi-nv/camera-ui/pygame/pg-picam-ui.py


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

Change the language, keyboard lang, and wifi lang if you'd like.

## Change the password for the pi user
`passwd`

## Add Startup/Shutdown button

Since WAKE_ON_GPIO is enabled in most RPI firmware by default, shorting GPIO3 (pin 5) to GND will wake the pi from sleep or power-off.  By enabling the gpio-shutdown overlay, you can have a single button connected between pin 5 and pin 6 to get a single Start/Shutdown button.
https://www.raspberrypi.org/forums/viewtopic.php?t=197495

Add the following line to /boot/config.txt
`dtoverlay=gpio-shutdown,gpio_pin=3`    // NOTE:gpio3 is the default pin for this overlay
OR (must be logged into the pi for next command)
`echo dtoverlay=gpio-shutdown,gpio_pin=3 | sudo tee -a /boot/config.txt`


## Make RPi USB-bootable
Once USB booting is enabled, it cannot be disabled.

`echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt`

This adds program_usb_boot_mode=1 to the end of /boot/config.txt. Reboot the Raspberry Pi with sudo reboot, then check that the OTP has been programmed with:

$ `vcgencmd otp_dump | grep 17:`
17:3020000a

### General Setup
```bash
# Update apt-get and install dependencies
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
#sudo apt-get upgrade -y
sudo apt-get install -y git python3-pip python3-dev python3-rpi.gpio python3-gpiozero python3-picamera python3-pygame python3-opencv

# Run test commands
pinout
pinout --monochrome
# Ex. check pinout on pi 3B+
pinout -r a020d3
# Ex. check pinout on pi zero W
pinout -r 9000c1

# Install tools and libs
#sudo apt-get install -y --fix-missing python3-pip
sudo apt-get install -y --fix-missing python3-picamera python3-pygame python3-opencv
# sudo apt -y --fix-broken install


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

Maybe?
```
hdmi_drive=2
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt 480 320 60 6 0 0 0
dtoverlay=ads7846,cs=1,penirq=25,penirq_pull=2,speed=50000,keep_vref_on=0,swapxy=0,pmax=255,xohms=150,xmin=200,xmax=3900,ymin=200,ymax=3900
start_x=1
gpu_mem=128
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

### Enable the camera

Login to the pi
Run `sudo raspi-config`
Enable the camera
Reboot the pi


### Wake the screen from the command line if screensaver is enabled
https://superuser.com/questions/942228/screen-saver-on-and-off-at-raspberry-pi-script-in-python

Install the x11-xserver-utils package to get the xset command. Then you can use it to force the DPMS signals to the monitor to on or off. You may need to set the DISPLAY variable in the environment. Eg:

DISPLAY=:0 xset dpms force on
sleep 10
DISPLAY=:0 xset dpms force off

You can do something like this in python. Poll every second. Remember if you have set the display on or off. Note the time-of-day whenever your signal is active. When the time since last active is over 2 minutes, switch display off. Loosely:

import os, subprocess, time
os.environ['DISPLAY'] = ":0"

displayison = False
maxidle = 2*60 # seconds
lastsignaled = 0
while True:
    now = time.time()
    if GPIO.input(PIR):
        if not displayison:
            subprocess.call('xset dpms force on', shell=True)
            displayison = True
        lastsignaled = now
    else:
        if now-lastsignaled > maxidle:
            if displayison:
                subprocess.call('xset dpms force off', shell=True)
                displayison = False
    time.sleep(1)

If you are interacting with the screen, and want it to stay on during this time independently of your gpio, you are probably better off letting the standard X11 idle mechanism detect that 2 minutes idle have elapsed and so automatically switching the screen off. Just use your program to force the screen on.

You can set a 120 second idle timeout with a single call of:

xset dpms 120 120 120
and can then remove the force off from the python.


### Configure pi for use with usb pi zero dongle
After mounting microsd, with os installed for the pi, into USB
1. Edit cmdline.txt in the boot folder/partition. Add "modules-load=dwc2,g_ether" after "rootwait"
2. Create a new file named "ssh" in the boot folder.
3. Eject microSD from computer, plug it into the pi zero
4. Plug pizero usb dongle into usb port of computer and wait for it to complete booting
5. Should be able to ssh into "raspberrypi.local". Ex. `ssh pi@raspberrypi.local`.
