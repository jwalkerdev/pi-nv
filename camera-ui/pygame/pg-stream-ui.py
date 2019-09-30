import os
import pygame
from pygame.locals import *
import cv2
import numpy as np
import datetime

'''
UI Layout:
Tall thin left panel: Leftmost 10-20% of screen
    Contains buttons: stop_preview, start_preview, save_image
Remaining screen used for video display

Todo:
* Implement video start/stop buttons
* Implement button visual change when pressed
* Update component to scale out if resolution is greater than a certain size.
* Use timeit to verify some different methods of retrieving and displaying video.
    https://pythonhow.com/measure-execution-time-python-code/
    https://docs.python.org/2/library/timeit.html
    https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
    VideoCapture options
        https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set
        ex. CV_CAP_PROP_CONVERT_RGB - whether or not to convert to RGB
    Test using camera directly.
    Make new class for each method. Test and report methodically.
    Use matplotlib to generate a diagram reporting results.
* display a splash screen until loading is done

Code referenecs:
https://github.com/Mekire/pygame-button
https://github.com/facelessloser/night_vision_pi/blob/master/camera_app/camera.py
https://learn.adafruit.com/pages/697/elements/83233/download (pyscope.py)
https://github.com/adafruit/adafruit-pi-cam
'''

# Either find the correct framebuffer device (/dev/fb0 or /dev/fb1) and set 
#   it here or set it as an env variable.
# Before running, on command line, set env var DISPLAY. Run `export DISPLAY=0:0` or `export DISPLAY=:0`
#   or set it here.
os.environ["SDL_FBDEV"] = "/dev/fb0"

# Initialize variables
screen = None
clock = None
components = []
event_consumers = []

# Initialize pygame
pygame.init()

# Get native display info from display.Info() by calling it before running first display.set_mode()
native_info = pygame.display.Info()
res_native = (native_info.current_w, native_info.current_h)
res_800_600 = (800,600)
s_flags = 0
if native_info.current_w < 800:
    s_res = res_native
    s_flags = pygame.FULLSCREEN
else:
    s_res = res_800_600

s_width  = s_res[0]
s_height = s_res[1]

# Colors
RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)
BRIGHTISH_GREEN = (30,230,30)


def main():
    global screen, clock
    "Ininitializes a new pygame screen using the framebuffer"
    verify_drivers()   # Configure and verify any rqeuired drivers
    
    # Initialize clock
    clock = pygame.time.Clock()

    # Initialize screen
    screen = pygame.display.set_mode((s_width, s_height), s_flags)
    pygame.display.set_caption('MJPEG Stream UI')

    # Draw and blit background and text
    draw_background()
    # Draw Initial Screen
    pygame.display.flip()

    # Add components
    
    # Add MJPEG stream viewer
    #   Ex. Safe public mjpeg stream for testing:  http://72.48.231.13/mjpg/video.mjpg
    viewer_rect = pygame.Rect(50,0,s_width-50,s_height)
    a_url = r'http://192.168.1.36:8000/stream.mjpg'
    viewer_obj = MJPEGStreamViewer(viewer_rect, a_url)
    components.append(viewer_obj)
    
    # Add TextLabel
    # label_rect1 = pygame.Rect(4,4,40,20)
    # components.append(TextLabel(label_rect1,text="Label"))
    
    # Add Start Button
    btn_rect1 = pygame.Rect(4,4,40,20)
    btn1 = Button(btn_rect1,text="Start")
    components.append(btn1)
    event_consumers.append(btn1)
    # Add Stop Button
    btn_rect2 = pygame.Rect(4,30,40,20)
    btn2 = Button(btn_rect2,text="Stop")
    components.append(btn2)
    event_consumers.append(btn2)
    
    # Run event loop
    event_loop()


def event_loop():
    # Event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
            for ec in event_consumers:
                ec.check_event(event)
                if btn1.clicked:
                    btn1.drawborder = 
                    btn2.drawborder 

        for c in components:
            c.draw()
        pygame.display.update()
        clock.tick(24)


class MJPEGStreamViewer:
    def __init__(self, rect, stream_url):
        self.noframe_count = 0
        self.rect = rect
        self.stream_url = stream_url
        # Initialize stream capture
        self.cap = cv2.VideoCapture(stream_url)
        if not self.cap.isOpened():
            print("Failure opening stream - {}.".format(stream_url))

    def draw(self):
        # Get and display MJPEG frame
        ret, frame = self.cap.read()
        if frame is None:
            self.noframe_count = self.noframe_count + 1
        else:
            self.noframe_count = 0
            # print("{} - frame read - {}".format(datetime.datetime.now(), ret))
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = frame.swapaxes(0,1)   # replaces np.rot90(frame)
            #frame = pygame.transform.scale(frame,(800,600))
            frame = pygame.surfarray.make_surface(frame)
            frame_size = frame.get_size()
            screen.blit(frame, self.rect, self.rect)
           

class TextLabel:
    ''' Simple TextLabel class:  rect, label text, color, bgcolor'''
    def __init__(self, rect, **kwargs):
        self.rect   = rect              # Boundary rect surface
        self.color   = (10,10,10)       # text color
        self.bgcolor = BRIGHTISH_GREEN  # bg color
        self.text   = '>'               # text
        if kwargs:
            for key, value in kwargs.items():
                if   key == 'color'   : self.color    = value
                elif key == 'bgcolor' : self.bgcolor  = value
                elif key == 'text'    : self.text     = value
        # Create font
        self.font = pygame.font.Font(None, 16)
        # Create and fill label background surface
        self.bg = pygame.Surface((self.rect.width, self.rect.height)).convert()

    def draw(self):
        self.bg.fill(self.bgcolor)
        text = self.font.render(self.text, 1, self.color)
        textpos = text.get_rect()
        textpos.centerx = self.bg.get_rect().centerx
        textpos.centery = self.bg.get_rect().centery
        self.bg.blit(text, textpos)
        screen.blit(self.bg, self.rect)


class Button:
    ''' Simple Button class:  rect, label text, color, bgcolor, callback
        Similar to TextLabel. Event handling added.
    '''
    def __init__(self, rect, **kwargs):
        self.rect     = rect              # Boundary rect
        self.color    = (10,10,10)        # text color
        self.bgcolor  = BRIGHTISH_GREEN   # bg color
        self.text     = '>'               # text
        self.callback = None              # Callback function
        if kwargs:
            for key, value in kwargs.items():
                if   key == 'color'    : self.color    = value
                elif key == 'bgcolor'  : self.bgcolor  = value
                elif key == 'text'     : self.text     = value
                elif key == 'callback' : self.callback = value
        # Create font
        self.font = pygame.font.Font(None, 16)
        # Create background surface
        self.bg = pygame.Surface((self.rect.width, self.rect.height)).convert()
        self.clicked = False
        self.drawborder = False

    def check_event(self, event):
        '''Receive and process events from event loop'''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mousedown(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_mouseup(event)

    def handle_mousedown(self, event):
        '''Handle mouse down event'''
        #print('Mouse down')
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            print('{} - Button click detected'.format(self.text))

    def handle_mouseup(self, event):
        '''Handle mouse up event. By default, callback function is called on mouse up.'''
        if self.clicked:
            if not self.callback == None:
                self.callback()
        self.clicked = False

    def draw(self):
        # Add border if selected
        self.bg.fill(self.bgcolor)
        # Add text
        text = self.font.render(self.text, 1, self.color)
        textpos = text.get_rect()
        textpos.center = self.bg.get_rect().center
        # textpos.centerx = self.bg.get_rect().centerx
        # textpos.centery = self.bg.get_rect().centery
        self.bg.blit(text, textpos)
        screen.blit(self.bg, self.rect)
        if self.drawborder:
            print('Trying to draw border')
            pygame.draw.rect(screen, RED, self.rect.inflate(-2,-2), 4)


def draw_background():
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BLACK)
    screen.blit(background, (0, 0))


def verify_drivers():
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


if __name__ == '__main__':
    main()
