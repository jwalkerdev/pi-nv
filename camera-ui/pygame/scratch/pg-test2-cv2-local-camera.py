'''
https://stackoverflow.com/questions/19240422/display-cv2-videocapture-image-inside-pygame-surface

The cv2 function camera.read() returns a BGR image, but the pygame.surfarray expects a RGB image.
'''

import pygame
from pygame.locals import *
import cv2
import numpy

color=True
camera_index = 0
camera=cv2.VideoCapture(camera_index)
camera.set(3,640)
camera.set(4,480)

#This shows an image the way it should be
cv2.namedWindow("w1",cv2.CV_WINDOW_AUTOSIZE)
retval,frame=camera.read()
frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
if not color:
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
cv2.flip(frame,1,frame)#mirror the image
cv2.imshow("w1",frame)

#This shows an image weirdly...
screen_width, screen_height = 640, 480
screen=pygame.display.set_mode((screen_width,screen_height))

def getCamFrame(color,camera):
    retval,frame=camera.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    if not color:
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
    cv2.flip(frame,1,frame) #mirror the image
    frame=numpy.rot90(frame)
    frame=pygame.surfarray.make_surface(frame) #I think the color error lies in this line?
    return frame

def blitCamFrame(frame,screen):
    screen.blit(frame,(0,0))
    return screen

screen.fill(0) #set pygame screen to black

running=True
while running:
    for event in pygame.event.get(): #process events since last loop cycle
        if event.type == KEYDOWN:
            running=False
    frame=getCamFrame(color,camera)
    screen=blitCamFrame(frame,screen)
    pygame.display.flip()

pygame.quit()
cv2.destroyAllWindows()