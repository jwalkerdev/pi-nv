# pi-nv


References:
* https://hackaday.io/project/27544-night-vision-camera-raspberry-pi/details

Pygame code based on ...
* https://learn.adafruit.com/pi-video-output-using-pygame?view=all
    * https://learn.adafruit.com/pages/697/elements/83233/download (pyscope.py)
    * https://learn.adafruit.com/pages/699/elements/83276/download (pyscope-animated.py)
* https://gist.github.com/radames/f7b46828929c78bd66b5


## Pi Setup Steps

Assumes that the picamera and VMP400 LCD display have already been connected to the pi.

```bash
# Install LCD-show
sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD-show

# Install python libs
sudo apt-get update
sudo apt-get install python3-picamera
sudo apt-get install python3-pip
sudo apt-get install python3-pygame
sudo apt-get install python3-opencv
sudo apt-get install python-picamera
sudo apt-get install python-pip
sudo apt-get install python-pygame
sudo apt-get install python-opencv

# Insert usb drive with files if one is needed
mkdir -p /mnt/usb
mount /dev/sda1 /mnt/usb

# Get code
mkdir -p ~/code
cd ~/code
git clone https://github.com/jwalkerdev/pi-nv.git
cd pi-nv

# Add to opencv py script and ui.py … os.environ["SDL_FBDEV"] = "/dev/fb1”
# Run ui.py 
sudo FRAMEBUFFER=/dev/fb1 python pyscope.py
# Run video script
sudo FRAMEBUFFER=/dev/fb1 python opencv_video_to_pygame_raspberry_pi.py
```
