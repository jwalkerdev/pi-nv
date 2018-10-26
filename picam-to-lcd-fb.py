
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

# Frame Buffer Toggle
use_fbdev = True

# Set SDL / Frame buffer env var
if use_fbdev:
    os.environ["SDL_FBDEV"] = "/dev/fb1"

# cam_width = 640
# cam_height = 480
cam_width = 1920
cam_height = 1080

screen_width = 480
screen_height = 320

camera = picamera.PiCamera()
print "Resolution: " + str(camera.resolution)
#camera.resolution = (cam_width, cam_height)
camera.resolution = '1080p'
print "Resolution: " + str(camera.resolution)
camera.hflip = True # Flip the video from the camera
camera.framerate = 30 # Frame rate
camera.exposure_mode = 'night'

pygame.display.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")

screen = pygame.display.set_mode([screen_width, screen_height])
video = picamera.array.PiRGBArray(camera)

try:
    for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):
        frame = np.rot90(frameBuf.array)        
        video.truncate(0)
        frame = pygame.surfarray.make_surface(frame)
        scaleVideo = pygame.transform.scale(frame, (480, 320)) # Scales the video to fit the screen
        #flipVideo = pygame.transform.flip(scaleVideo, False, False) # Flip the scaled video horizonatly; args (vide, horiz, vert)
        screen.fill([0,0,0])
        #screen.blit(flipVideo, (0,0))
        screen.blit(scaleVideo, (0,0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                    raise KeyboardInterrupt
except KeyboardInterrupt,SystemExit:
    pygame.quit()
    cv2.destroyAllWindows()