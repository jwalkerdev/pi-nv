import pygame
from pygame.locals import *
import cv2
import numpy as np
import datetime

'''
The cv2 function capture_object.read() returns a BGR image, but the pygame.surfarray expects a RGB image.

Different approach using pygame.image.frombuffer(...) :
    https://stackoverflow.com/questions/27805077/display-io-stream-from-raspberry-pi-camera-as-video-in-pygame
'''

def main():
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
