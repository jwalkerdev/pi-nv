import pygame
from pygame.locals import *
import cv2
import numpy as np
import datetime

### Doc
'''
Resolution Info:
DVD: 720x480
720p: 1280x720
1080p: 1920x1080
Ultra HD(4k): 3840x2160
NTSC: 640x360 (16/9)
PAL: 720x405 (16/9)
HDTV: 1280x720, 1920x1080

Parts Used:
    - LCD
        - Velleman VMP400 320x480 SPI LCD
        - interfaces with rpi gpio ports
    - Camera
        - smraza: Camera Module for Raspberry Pi 3 with 5MP 1080p OV5647 Video Webcam
            - https://www.amazon.com/gp/product/B073183KYK
            - Supports Night Vision Compatible with Raspberry Pi 3b 2 Model B B+
            - Image resolution:  1080p / 1920x1080
                - Scale ratio to 480x320:   4x3.375
                - Scaled resolutions:
                    - 1440x960 (3x)
                    - 1620x1080 (3.375x)
            - Video modes
                1080p30 (1920x1080 @ 30 fps)
                720p60 (1280x720 @ 60 fps)
                640 x 480p60/90
'''

'''
The cv2 function capture_object.read() returns a BGR image, but the pygame.surfarray expects a RGB image.

Different approach using pygame.image.frombuffer(...) :
    https://stackoverflow.com/questions/27805077/display-io-stream-from-raspberry-pi-camera-as-video-in-pygame


How to get Native screen resolution:
    https://stackoverflow.com/questions/19954469/how-to-get-the-resolution-of-a-monitor-in-pygame
    You can use pygame.display.Info():

    The docs say:

    current_h, current_w: Height and width of the current video mode, or of the desktop mode if called before the display.set_mode is called.
    (current_h, current_w are available since SDL 1.2.10, and pygame 1.8.0) They are -1 on error, or if an old SDL is being used.1.8.0)

    pygame.display.Info() creates an Info Object with the attributes current_h and current_w. Create the Info Object before you call display.set_mode and then call display.set_mode with current_h and current_w from the object.

    Example:
    infoObject = pygame.display.Info()
    pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
'''

# Either find the correct framebuffer device (/dev/fb0 or /dev/fb1) and set 
#   it here or set it as an env variable.
# Before running, on command line, set env var DISPLAY. Run `export DISPLAY=0:0`
#   or set it here.
os.environ["SDL_FBDEV"] = "/dev/fb0"

# Get native display info before running first display.set_mode()
infoObject = pygame.display.Info()
native_res_w = infoObject.current_w
native_res_h = infoObject.current_h
native_res = (native_res_w, native_res_h)

# Initialize potential screen sizes

res_dvd = (720, 480)
res_720p = (1280, 720)
res_1080p = (1920 ,1080)
res_ultraHD_4k = (3840, 2160)
res_ntsc = (640,360)  # (16/9)
res_pal = (720,405)  # (16/9)
res_hdtv = (1280,720) 
res_hdtv2 = (1920,1080)

# Initialize fonts

def main():

    "Ininitializes a new pygame screen using the framebuffer"
    # Based on "Python GUI in Linux frame buffer"
    # http://www.karoltomala.com/blog/?p=679
    disp_no = os.getenv("DISPLAY")
    if disp_no:
        print ("I'm running under X display = {0}".format(disp_no))
    
    # Check which frame buffer drivers are available
    # Start with fbcon since directfb hangs with composite output
    drivers = ['fbcon', 'directfb', 'svgalib']
    found = False
    for driver in drivers:
        # Make sure that SDL_VIDEODRIVER is set
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        try:
            pygame.display.init()
        except pygame.error:
            print('Driver: {0} failed.'.format(driver))
            continue
        found = True
        break

    if not found:
        raise Exception('No suitable video driver found!')

    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print "Framebuffer size: %d x %d" % (size[0], size[1])
    self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)



    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 800), RESIZABLE)
    pygame.display.set_caption('MJPEG live feed')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    #background.fill((250, 250, 250))  # White-ish
    background.fill(Color('black'))  # Black

    # Display some text
    # font = pygame.font.Font(None, 36)
    # text = font.render("Hello There", 1, (10, 10, 10))
    # textpos = text.get_rect()
    # textpos.centerx = background.get_rect().centerx
    # background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # Initialise clock
    clock = pygame.time.Clock()

    # Initialize stream capture
    #cap = cv2.VideoCapture('http://72.48.231.13/mjpg/video.mjpg')
    cap = cv2.VideoCapture('http://192.168.1.36/stream.mjpg')
    ret, frame = cap.read()
 
    frame_size = ''

    # Event loop
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
    
        # Get and display MJPEG frame
        ret, frame = cap.read()
        if frame is not None:
            # print("{} - frame read - {}".format(datetime.datetime.now(), ret))
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = frame.swapaxes(0,1)   # replaces np.rot90(frame)
            #frame = pygame.transform.scale(frame,(800,600))
            frame = pygame.surfarray.make_surface(frame)
            frame_size = frame.get_size()
            screen.blit(frame, (0, 0))
            pygame.display.flip()
    
    print('MJPEG frame size: {}'.format(frame_size))
    pygame.quit()


if __name__ == '__main__': main()
