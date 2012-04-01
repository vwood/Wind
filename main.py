#!/usr/bin/env python2

import ode
from pgu import gui as pgui
import pygame
from pygame.locals import *

# TODO: I would prefer objects... with editable text.
def blit_text(surface, text, x=None, y=None, size=12, color=(255, 255, 255)):
    """Display a string on a surface at x & y.
    If either of x or y are not set,
    the text is centered on that axis."""
    font = pygame.font.Font(None, size) # Fonts should be stored in some form of resource management (env)
    text = font.render(text, True, color) # True for antialiasing
    if x == None:
        x = surface.get_width() / 2
    if y == None:
        y = surface.get_height() / 2
    pos = text.get_rect(centerx = x, centery = y)
    surface.blit(text, pos)

    
class TextBox(object):
    """A box that contains text."""
    # TODO: store as a list of lines
    # store cursor position
    def __init__(self, contents="", width=32, height=1, font_size=12):
        self.width, self.height = width, height
        self.contents = contents.split("\n")
        self.font_size = font_size

    def display(self, surface, x, y):
        """Display the text box on a surface."""
        blit_text(surface, self.get_contents(), x, y, self.font_size)

    def get_contents(self):
        """Get the contents as a single string."""
        return "\n".join(self.contents)
        
    
class Engine(object):
    """Base engine for running the system."""
    def __init__(self, width=640, height=240):
        super(Engine, self).__init__()
        pygame.init()
        if not pygame.font:
            exit()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Engine")
        self.clock = pygame.time.Clock()
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 10, 30))
        self.screen.blit(self.background, (0, 0))
        text = TextBox("Bums")
        text.display(self.screen, 80, 80)
        blit_text(self.screen, "Bums", 20, 20, 20, (200,200,200))
        self.gui = pgui.App()
        container = pgui.Container()
        container.add(pgui.TextArea("", 300, 200, 12), x=0, y=0)
        container.add(pgui.TextArea("", 300, 200, 12), x=300, y=0)
        self.gui.init(widget = container)
        pygame.display.flip()
#        self.gui.run()
        
    def run(self):
        """Mainloop for catching events and performing updates."""
        while True:
            self.clock.tick(60)
            self.gui.loop()
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    else:
                        event.unicode

                        
if __name__ == '__main__':
    e = Engine()
    e.run()

