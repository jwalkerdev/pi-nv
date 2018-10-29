# pi-nv


References:
* https://hackaday.io/project/27544-night-vision-camera-raspberry-pi/details

Pygame code based on ...
* https://learn.adafruit.com/pi-video-output-using-pygame?view=all
    * https://learn.adafruit.com/pages/697/elements/83233/download (pyscope.py)
    * https://learn.adafruit.com/pages/699/elements/83276/download (pyscope-animated.py)
* https://gist.github.com/radames/f7b46828929c78bd66b5


## Install Raspbian Stretch Lite

Write image to SD card with Etcher.

Assuming, the SD gets mounted to /Volumes/boot on the local system (osx for me), run the following commands:
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
END_OF_FILE) > wpa_supplicant.conf



## VMP400 - Pi Setup Steps

Assumes that the picamera and VMP400 LCD display have already been connected to the pi.

```bash
# Update apt-get and install git
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y git

# Get project code
mkdir -p ~/code
cd ~/code
git clone https://github.com/jwalkerdev/pi-nv.git
cd pi-nv

# Install LCD-show
sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD35-show

# Install tools and libs
sudo apt-get install -y --fix-missing python-pip 
sudo apt-get install -y --fix-missing python-picamera 
sudo apt-get install -y --fix-missing python-pygame 
sudo apt-get install -y --fix-missing python-opencv
sudo apt-get install -y --fix-missing python3-pip 
sudo apt-get install -y --fix-missing python3-picamera 
sudo apt-get install -y --fix-missing python3-pygame 
sudo apt-get install -y --fix-missing python3-opencv


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

## Installing Kuman 3.5in HDMI display

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
curl -k -O https://www.dropbox.com/s/jrw8bnb4vswo309/LCD-show.tar.gz

# Unpack the file and set permissions
tar xzf LCD-show.tar.gz
chmod +x LCD* MPI*show

cd /boot
cp LCD-show.tar.gz ~
cd ~
sudo tar zxvf LCD-show.tar.gz
cd LCD-show/
sudo ./MPI3508_480_320-show
```

```bash
# Download rpi_camera_surveillance_system.py
curl -O -k https://raw.githubusercontent.com/RuiSantosdotme/Random-Nerd-Tutorials/master/Projects/rpi_camera_surveillance_system.py
# Run it
python3 rpi_camera_surveillance_system.py
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
