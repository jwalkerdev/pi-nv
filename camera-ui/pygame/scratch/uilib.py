import pygame

screen = None

class TextLabel:
    ''' Simple TextLabel class:  rect, label text, color, bgcolor'''
    def __init__(self, rect, **kwargs):
        self.rect   = rect              # Boundary rect surface
        self.color   = (10,10,10)       # text color
        self.bgcolor = (250,250,250)  # bg color
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
    ''' Button class:  rect, label text, color, bgcolor, callback
    '''
    def __init__(self, rect, **kwargs):
        self.rect     = rect              # Boundary rect
        self.color    = (10,10,10)        # text color
        self.bgcolor  = (230,230,230)     # bg color
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

    def check_event(self, event):
        '''Receive and process events from event loop'''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mousedown(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_mouseup(event)

    def handle_mousedown(self, event):
        '''Handle mouse down event'''
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
        self.bg.fill(self.bgcolor)
        text = self.font.render(self.text, 1, self.color)
        textpos = text.get_rect()
        textpos.center = self.bg.get_rect().center
        self.bg.blit(text, textpos)
        screen.blit(self.bg, self.rect)


class ButtonWithRedBorderOnClick:
    ''' Simple Button class:  rect, label text, color, bgcolor, callback
        Similar to Button. Border alternates being draw and not drawn
        on every other click.
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
            self.drawborder = True
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
