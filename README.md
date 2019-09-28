# pi-nv


References:
* https://hackaday.io/project/27544-night-vision-camera-raspberry-pi/details
    * https://hackaday.io/project/27544-night-vision-camera-raspberry-pi
    * https://github.com/facelessloser/night_vision_pi/blob/master/camera_app/camera.py
* Referenced by the hackaday project https://gist.github.com/radames/f7b46828929c78bd66b5


Pygame code based on ...
* https://learn.adafruit.com/pi-video-output-using-pygame?view=all
    * https://learn.adafruit.com/pages/697/elements/83233/download (pyscope.py)
    * https://learn.adafruit.com/pages/699/elements/83276/download (pyscope-animated.py)
* https://gist.github.com/radames/f7b46828929c78bd66b5
* https://github.com/adafruit/adafruit-pi-cam
* https://github.com/facelessloser/night_vision_pi/blob/master/camera_app/camera.py


## URLs to review for pygame and camera uis

https://www.digikey.com/en/maker/blogs/2018/the-best-gui-widgets-for-raspberry-pi
https://github.com/local-vision/Pi-Vision
https://github.com/Billwilliams1952/PiCameraApp/blob/master/Source/PiCameraApp.py
http://idlelogiclabs.com/2016/10/10/raspberry-pi-3-camera-windowed-preview/
https://www.tutorialspoint.com/wxpython/wxpython_hello_world.htm
https://pypi.org/project/wxPython/
https://wiki.wxpython.org/
https://www.raspberrypi.org/forums/viewtopic.php?p=374577
https://github.com/sixbacon/RPICameraGUI
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://www.datacamp.com/community/tutorials/gui-tkinter-python
https://www.geeksforgeeks.org/python-gui-tkinter/
https://docs.wxwidgets.org/3.1/overview_python.html
https://projects.raspberrypi.org/en/projects/getting-started-with-guis


## Install Raspbian Lite

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

## General Setup
```bash
# Update apt-get and install git
sudo apt-get update
#sudo apt-get upgrade -y
sudo apt-get install -y git
# Install pip
sudo apt-get install -y python-pip python3-pip

# Install RPi.GPIO
sudo apt-get install -y python-dev python-rpi.gpio python3-dev python3-rpi.gpio
# Install gpiozero for the tools and libs
sudo apt-get install -y python-gpiozero python3-gpiozero

# Run test commands
pinout
pinout --monochrome
# Or forced to be --color, in case you are redirecting to something capable of supporting ANSI codes:
pinout --color | less -SR
# Can check pinout for any particular pi version
# https://elinux.org/RPi_HardwareHistory
# Ex. check pinout on pi 3B+
pinout -r a020d3
# Ex. check pinout on pi zero W
pinout -r 9000c1

# Get project code
mkdir -p ~/code
cd ~/code
git clone https://github.com/jwalkerdev/pi-nv.git
git clone
cd pi-nv

# Install tools and libs
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
```

## Optional Pi Setup Steps (used for testing and misc tasks)
```bash
# Insert usb drive with files if one is needed
mkdir -p /mnt/usb
mount /dev/sda1 /mnt/usb

# Add to opencv py script and ui.py … os.environ["SDL_FBDEV"] = "/dev/fb1”
# Run ui.py 
# sudo FRAMEBUFFER=/dev/fb1 python pyscope.py
sudo python pyscope.py
# Run video script
sudo python opencv_video_to_pygame_raspberry_pi.py
# Run picam-to-lcd script
sudo picam-to-lcd.py
```

```bash
cd code
# Download rpi_camera_surveillance_system.py
curl -O -k https://raw.githubusercontent.com/RuiSantosdotme/Random-Nerd-Tutorials/master/Projects/rpi_camera_surveillance_system.py
# Run it
python3 rpi_camera_surveillance_system.py
```

## VMP400 - Pi Setup Steps

Assumes that the picamera and VMP400 LCD display have already been connected to the pi.

```bash
# Install LCD-show
sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD35-show
```

## Installing Kuman 3.5in HDMI display

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

Now, reboot the pi

#### Install drivers and enable LCD

```bash
# On public network, run this. Otherwise, manually copy the drivers to the pi
curl -L -k -O https://www.dropbox.com/s/jrw8bnb4vswo309/LCD-show.tar.gz

# Unpack the file and set permissions
tar xzf LCD-show.tar.gz
cd LCD-show
chmod +x LCD* MPI*show
sudo ./MPI3508_480_320-show
```

### Waveshare directions (tried these because I couldn't find Kuman docs at first)
```bash
################################################################
# Waveshare LCD directions
# https://www.waveshare.com/wiki/3.5inch_HDMI_LCD
# https://www.waveshare.com/wiki/5inch_HDMI_LCD

cd /tmp

# This driver is for Raspbian after 180303 version. Network connection is required when installing.
curl -k -O https://www.waveshare.com/w/upload/1/1e/LCD-show-180817.tar.gz
tar xzf LCD-show-180817.tar.gz
mv LCD-show LCD-show-180817
# If you want to use Raspbian Lite version or switch to Console mode, please download this driver instead
curl -k -O https://www.waveshare.com/w/upload/0/00/LCD-show-170703.tar.gz
tar xzf LCD-show-170703.tar.gz
mv LCD-show LCD-show-170703

mv LCD-show-170703 ~
mv LCD-show-180817 ~
```


## Pi Zero - Connect with USB cable

https://medium.com/@aallan/setting-up-a-headless-raspberry-pi-zero-3ded0b83f274
https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/
More information on networking over USB on Linux can be found at http://www.linux-usb.org/usbnet/ .

### Configure Raspbian to treat the USB port like an ethernet port. 

* Mount the micro SD card in a computer (not Pi Zero) and open it with Finder, or Windows Explorer, or whatever it is that you use.
* Edit `<mnt_root>/config.txt` on the mounted drive. This sets us up for the next file we need to edit
In this file you want to add the following line at the very bottom:   
```dtoverlay=dwc2```
* On the mounted drive, edit `<mnt_root>/cmdline.txt`.  Note: Parameters in this file are not delimited by new lines or commas, they are delimited by space characters - so don't add extra spaces.
After the `rootwait` parameter, add the following parameter...   
```modules-load=dwc2,g_ether```
* Enable SSH. Create a file called `ssh` and save it to the root directory of the boot mount on the SD card. The file can be blank.

To connect to the Raspberry Pi Zero over USB you’ll need Bonjour or similar installed on your host computer. I’m using a Mac so I was fortunate enough to already be in the clear. For Windows you should be fine installing iTunes or QuickTime and for Linux the Avahi Daemon. Many Linux distributions should have it already installed.

With it installed, power on the Pi Zero with the USB data cable. I made sure to use the port labeled USB, not PWR. This port allows you to power the Pi Zero and do data transfer. Once connected, give it some time because it will have to configure some things for the first time.

* Plug the USB cable into the USB port (not the PWR) port.
This will supply power to the pi zero and will also create a data connection.
* Find the IP of the pi zero locally:
    dns-sd -G v4 raspberrypi.local
* ssh pi@<IP address found in the previous step>


## Pi Zero Troubleshooting

`iwgetid` - get SSID of currently connected wifi connection
`iwconfig` - display or configure wifi


## Lipo Battery Info

A profile of the voltage for a 'classic' 3.7V/4.2V battery. The voltage starts at 4.2 maximum and quickly drops down to about 3.7V for the majority of the battery life. Once you hit 3.4V the battery is dead and at 3.0V the cutoff circuitry disconnects the battery (more on that later.

https://learn.adafruit.com/li-ion-and-lipoly-batteries/voltages

https://learn.adafruit.com/assets/979


## ADC0832 Info
* http://wiki.sunfounder.cc/index.php?title=AD_Converter-ADC0832_Module
    * NOTE: This module is not the actual ADC0832. It is built around it. In particular, note that this board uses a single pin for the Input and Output pins of Microwire protocol used by the chip
* http://wiki.sunfounder.cc/images/1/1e/ADC0832_datasheet.pdf
* https://github.com/sunfounder/Sunfounder_SensorKit_Python_code_for_RaspberryPi/blob/master/ADC0832.py
* https://github.com/sahithyen/RPI_ADC0832
* https://gist.github.com/HeinrichHartmann/27f33798d12317575c6c

Pull-down resistors in any final connections that have floating values could be beneficial

## Miscellaneous Reference Material
* http://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
