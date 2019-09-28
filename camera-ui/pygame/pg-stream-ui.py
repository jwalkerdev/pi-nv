import os
import pygame
from pygame.locals import *

'''
Code referenecs:
https://github.com/Mekire/pygame-button
'''

# Either find the correct framebuffer device (/dev/fb0 or /dev/fb1) and set 
#   it here or set it as an env variable.
# Before running, on command line, set env var DISPLAY. Run `export DISPLAY=0:0` or `export DISPLAY=:0`
#   or set it here.
os.environ["SDL_FBDEV"] = "/dev/fb0"

# Initialize pygame
pygame.init()

# Get native display info from display.Info() by calling it before running first display.set_mode()
native_info = pygame.display.Info()
res_native = (native_info.current_w, native_info.current_h)
res_zero = (0,0)
res_600_600 = (600,600)


'''
# Initialize potential screen sizes
res_dvd = (720, 480)
res_720p = (1280, 720)
res_1080p = (1920 ,1080)
res_ultraHD_4k = (3840, 2160)
res_ntsc = (640,360)  # (16/9)
res_pal = (720,405)  # (16/9)
res_hdtv = (1280,720) 
res_hdtv2 = (1920,1080)
'''

#s_res = res_native
s_res = res_600_600
s_width  = s_res[0]
s_height = s_res[1]
s_flags = 0
# s_flags = pygame.FULLSCREEN

screen = None
clock = None
components = []

def main():
    global screen, clock
    "Ininitializes a new pygame screen using the framebuffer"
    verify_drivers()   # Configure and verify any rqeuired drivers
    
    # Initialize clock
    clock = pygame.time.Clock()

    # Initialize screen
    screen = pygame.display.set_mode(size=(s_width, s_height), flags=s_flags)
    pygame.display.set_caption('MJPEG Stream UI')

    # Draw and blit background and text
    bg = draw_background()
    display_some_text_on_bg(bg)
    # Add components
    components.append(TextLabel(20,20,80,40))
    # Draw Initial Screen
    pygame.display.flip()
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

        for c in components:
            c.draw()
        pygame.display.flip()
        clock.tick(1)


class TextLabel:
    ''' Simple TextLabel class:  rect, label, color, labelcolor
        Next version could use pygame.Rect(x,y,width,height) instead of separate params.
    '''
    def __init__(self, x, y, width, height, **kwargs):
        # self.rect   = rect      # Boundary rect surface
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height
        self.color   = (10,10,10)     # text color
        self.bgcolor = (30,230,30)   # bg color ; #1EE61E - bright-ish green
        self.text   = '>'      # text
        if kwargs:
            for key, value in kwargs.iteritems():
                if   key == 'color'   : self.color    = value
                elif key == 'bgcolor' : self.bgcolor  = value
                elif key == 'text'    : self.text     = value
        
        # Create font
        self.font = pygame.font.Font(None, 36)
        # Create and fill label background surface
        self.bg = pygame.Surface((self.width, self.height)).convert()
        self.counter = 0

    def draw(self):
        print("{} - {}".format("time", "drawing"))
        self.bg.fill(self.bgcolor)
        # Draw some text
        text = self.font.render("{} - {}".format(self.text, self.counter), 1, self.color)
        textpos = text.get_rect()
        textpos.centerx = self.bg.get_rect().centerx
        textpos.centery = self.bg.get_rect().centery
        self.bg.blit(text, textpos)
        screen.blit(self.bg, (self.x, self.y))
        self.counter = self.counter + 1

        # if self.text:
        #     text_rect = text.get_rect(center=self.rect.center)
        #     surface.blit(text,text_rect)


def draw_background():
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))  # Almost completely white
    screen.blit(background, (0, 0))
    return background

def display_some_text_on_bg(background):
    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

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
