import os
import pygame
from pygame.locals import *
import cv2
import numpy as np
import datetime
import math

'''
UI Layout:
Tall thin left panel: Leftmost 10-20% of screen
    Contains buttons: stop_preview, start_preview, save_image
Remaining screen used for video display

Todo:
* Done - Implement video start/stop buttons
* Done - Implement video transform to fill viewing area
* Done (could be improved) - Implement button visual change when pressed
* Add argparse to pass in the stream url and other options.
* Attempt transparent buttons with visible text.
* Add icon to flip image orientation vertical or horizontal
* Add icon to enable or disable mouse visibility
* Test using Picamera classes instead of OpenCV2 code
* Build pygame from source on destination system to get v1.9.5, with touch support
* Attempt clickable icons and/or shapes
* Update component to scale out if resolution is greater than a certain size.
* Implement brightness slider
* Performance
    Use timeit to verify some different methods of retrieving and displaying video.
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

Code references:
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
background = None
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
    print("Screen setup - flags: FULLSCREEN, resolution: {}".format(s_res))
else:
    s_res = res_800_600
    s_flags = pygame.RESIZABLE
    print("Screen setup - flags: RESIZABLE, resolution: {}".format(s_res))

s_width  = s_res[0]
s_height = s_res[1]

# Colors
RED = (200,0,0)
GREEN = (0,200,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)
BRIGHTISH_GREEN = (30,230,30)

btnStartStop = None
video_viewer = None

def main():
    global screen, clock, btnStartStop, video_viewer
    "Ininitializes a new pygame screen using the framebuffer"
    verify_drivers()   # Configure and verify any rqeuired drivers

    # Initialize clock
    clock = pygame.time.Clock()

    # Disable mouse visibility
    #pygame.mouse.set_visible(False)

    # Initialize screen
    screen = pygame.display.set_mode((s_width, s_height), s_flags)
    pygame.display.set_caption('MJPEG Stream UI')

    # Draw and blit background and text
    draw_background()
    # Draw Initial Screen
    pygame.display.update()

    # Add components

    # Add PiCamera viewer
    viewer_rect = pygame.Rect(50,0,s_width-50,s_height)
    video_viewer = Cv2LocalCameraViewer(viewer_rect)
    components.append(video_viewer)

    # Add Start Button
    btn_rect1 = pygame.Rect(4,4,45,45)
    initial_text = "Stop" if video_viewer.get_running() == True else "Start"
    btnStartStop = Button(btn_rect1,text=initial_text, callback=btnStartStop_callback)
    components.append(btnStartStop)
    event_consumers.append(btnStartStop)

    # Run event loop
    event_loop()


def btnStartStop_callback():
    if video_viewer is None or btnStartStop is None:
        return
    video_viewer.set_running(not video_viewer.get_running())
    running = video_viewer.get_running()
    if running:
        btnStartStop.set_text("Stop")
    else:
        btnStartStop.set_text("Start")


def event_loop():
    # Event loop
    click_pos = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                video_viewer.release()
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
                    video_viewer.release()
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
                click_pos = event.pos
            for ec in event_consumers:
                ec.check_event(event)

        draw_background()
        for c in components:
            c.draw()
        if click_pos:
            pygame.draw.rect(screen, BLUE, (click_pos[0]-5,click_pos[1]-5, 20, 20))
        pygame.draw.rect(screen, RED, screen.get_rect().inflate(-2,-2), 4)
        pygame.display.update()
        clock.tick(30)


class Cv2LocalCameraViewer:
    '''
        PicameraViewer class
        Expand video frame width to fill self.rect maximally and scale height by same scale factor.
        OpenCV VideoCapture properties:
            https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set
    '''
    def __init__(self, rect, **kwargs):
        self.noframe_count = 0
        self.rect = rect
        self.capture_enabled = True
        self.fps = 24
        if kwargs:
            for key, value in kwargs.items():
                if   key == 'capture_enabled' : self.capture_enabled = value

        # Initialize stream capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        #self.cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)
        if not self.cap.isOpened():
            print("Failure opening camera 0.")
            self.capture_enabled = False
        # Initialize font for stopped capture
        self.font = pygame.font.Font(None, int(self.rect.width / 12))
        # Create background surface
        self.bg = pygame.Surface((self.rect.width, self.rect.height)).convert()
        self.text_stopped = self.font.render("Stopped", 1, (220,220,220))
        # Initialize variable that will hold the scaled video height
        self.scaled_height = 0

    def set_running(self, enabled=True):
        self.capture_enabled = enabled

    def get_running(self):
        return self.capture_enabled

    def release(self):
        self.cap.release()

    def draw(self):
        # Get and display MJPEG frames (images) if video is enabled
        # image returned by CV2 is a numpy array
        if not self.capture_enabled:
            self.bg.fill((0,0,0))
            textpos = self.text_stopped.get_rect()
            textpos.center = self.bg.get_rect().center
            self.bg.blit(self.text_stopped, textpos)
            screen.blit(self.bg, self.rect)
        else:
            ret, img = self.cap.read()
            if not ret or img is None:
                self.noframe_count = self.noframe_count + 1
            else:
                self.noframe_count = 0
                # print("{} - frame read - {}".format(datetime.datetime.now(), ret))
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  # no longer needed after setting CV_CAP_PROP_CONVERT_RGB
                #img = np.rot90(img, 3)
                img = np.swapaxes(img,0,1)   # replaces np.rot90(frame)
                img = np.flipud(img)     # flip image array on the y-axis only
                img = np.fliplr(img)     # flip image array on the y-axis only, using fliplr because we already swapped axes
                # Calculate scaled width and height of video
                if self.scaled_height == 0:
                    frame_w, frame_h = img.shape[:2]   # getting dimensions of image, which is actually an ndarray
                    scale_factor = self.rect.width/frame_w
                    self.scaled_height = math.floor(frame_h * scale_factor / 2.0) * 2   # rounds down to nearest even int
                frame = pygame.surfarray.make_surface(img)
                frame = pygame.transform.scale(frame,(self.rect.width,self.scaled_height))
                screen.blit(frame, self.rect, self.rect)



class Button:
    ''' Button class:  rect, label text, color, bgcolor, callback
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

    def set_text(self, text):
        if text is None:
            self.text = ''
        else:
            self.text = text

    def check_event(self, event):
        ''' Receive and process events from event loop.
            Events handled:
              MOUSEBUTTONUP     pos, button
              MOUSEBUTTONDOWN   pos, button
              FINGERDOWN         touch_id, finger_id, x, y, dx, dy
              FINGERUP           touch_id, finger_id, x, y, dx, dy
            NOTE: FINGERDOWN and FINGERUP events not supported until pygame 1.9.5
        '''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mousedown(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_mouseup(event)
        # elif event.type == FINGERDOWN:
        #     self.handle_fingerdown(event)
        # elif event.type == FINGERUP:
        #     self.handle_fingerup(event)

    def handle_mousedown(self, event):
        '''Handle mousedown event'''
        #print('Mouse down')
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            print('{} - Button click detected'.format(self.text))

    def handle_mouseup(self, event):
        '''Handle mouse up event. By default, callback function is called on mouse/finger up.'''
        if self.clicked:
            if not self.callback == None:
                self.callback()
        self.clicked = False

    # def handle_fingerdown(self, event):
    #     '''Handle fingerdown event'''
    #     #print('Finger down')
    #     event_pos = (event.x, event.y)
    #     if self.rect.collidepoint(event_pos):
    #         self.clicked = True
    #         print('{} - Finger down (click) detected'.format(self.text))

    # def handle_fingerup(self, event):
    #     '''Handle finger up event. By default, callback function is called on mouse/finger up.'''
    #     if self.clicked:
    #         if not self.callback == None:
    #             self.callback()
    #     self.clicked = False

    def draw(self):
        # Add border if selected
        self.bg.fill(self.bgcolor)
        # Add text
        text = self.font.render(self.text, 1, self.color)
        textpos = text.get_rect()
        textpos.center = self.bg.get_rect().center
        self.bg.blit(text, textpos)
        screen.blit(self.bg, self.rect)
        # if self.drawborder:
        #     print('Trying to draw border')
        #     pygame.draw.rect(screen, RED, self.rect.inflate(-2,-2), 4)


def draw_background():
    global background
    # Fill background
    if not background:
        background = pygame.Surface(screen.get_size()).convert()
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
    if not found:
        raise Exception('No suitable video driver found!')


if __name__ == '__main__':
    main()
