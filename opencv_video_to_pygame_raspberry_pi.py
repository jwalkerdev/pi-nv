
import os
import pygame
from pygame.locals import *
import cv2
import numpy as np
import time
import picamera
import picamera.array

# Set SDL / Frame buffer env var
os.environ["SDL_FBDEV"] = "/dev/fb1"

# screen_width = 640
# screen_height = 480
screen_width = 480
screen_height = 320

camera = picamera.PiCamera()
camera.resolution = (screen_width, screen_height)

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")

screen = pygame.display.set_mode([screen_width, screen_height])
video = picamera.array.PiRGBArray(camera)

try:
    for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):
        frame = np.rot90(frameBuf.array)        
        video.truncate(0)
        frame = pygame.surfarray.make_surface(frame)
        screen.fill([0,0,0])
        screen.blit(frame, (0,0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                    raise KeyboardInterrupt
except KeyboardInterrupt,SystemExit:
    pygame.quit()
    cv2.destroyAllWindows()