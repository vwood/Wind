#!/usr/bin/env python2

import pgu
import pygame
from pygame.locals import *

def blit_text(surface, text, x, y, size, color):
    """TODO: I would prefer objects... with editable text.
    Also I'd like to get rid of the 'center' handling."""
    font = pygame.font.Font(None, size) # Fonts should be stored in some form of resource management (env)
    text = font.render(text, True, color) # True for antialiasing
    if x == "center":
        x = surface.get_width() / 2
    if y == "center":
        y = surface.get_height() / 2
    pos = text.get_rect(centerx = x, centery = y)
    surface.blit(text, pos)


class Engine(object):
    """Base engine for running the system."""
    def __init__(self, width=320, height=240):
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
        blit_text(self.screen, "Bums", 20, 20, 20, (200,200,200))
        pygame.display.flip()

    def run(self):
        """Mainloop for catching events and performing updates."""
        while True:
            self.clock.tick(60)
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

