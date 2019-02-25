
import os
import pygame
from pygame.locals import *
import cv2
import numpy as np
import time
import picamera
import picamera.array

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
            - Max resolution:  1080p / 1920x1080
                - Scale ratio to 480x320:   4x3.375
                - Scaled resolutions:
                    - 1440x960 (3x)
                    - 1620x1080 (3.375x)
'''


# Set SDL / Frame buffer env var
os.environ["SDL_FBDEV"] = "/dev/fb1"

# screen_width = 640
# screen_height = 480
screen_width = 480
screen_height = 320

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")

if pygame.display.Info().current_w < 500:
    ui_panel_size = 80
else:
    ui_panel_size = pygame.display.Info().current_w * 20 / 100

fullscreen_bool = True
if fullscreen_bool:
    # FULLSCREEN
    screen_size = (pygame.display.Info().current_w - ui_panel_size, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
else:
    # Specific Screen Size
    screen_size = (screen_width - ui_panel_size, screen_height)
    screen = pygame.display.set_mode(screen_size)

camera = picamera.PiCamera()
camera.hflip = True # Flip the video from the camera
#camera.framerate = 30 # Frame rate
camera.exposure_mode = 'night'
camera.resolution = screen_size
video = picamera.array.PiRGBArray(camera)

try:
    for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):
        frame = np.rot90(frameBuf.array)        
        video.truncate(0)
        frame = pygame.surfarray.make_surface(frame)
        screen.fill([ui_panel_size,0,0])
        screen.blit(frame, (0,0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                    raise KeyboardInterrupt

except KeyboardInterrupt,SystemExit:
    pygame.quit()
    cv2.destroyAllWindows()