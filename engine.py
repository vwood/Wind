#!/usr/bin/env python2

import pygame
from pygame.locals import *

import game


# TODO: there's a window widget trapped in here,
# along with a game runner. Separate them.
class Engine(object):
    contents = None
    
    """Base engine for running the system."""
    def __init__(self, **kwargs):
        """Creates an engine object.
        Keywords are:
        width, height = Size of the window
        caption = Caption of the window
        back_color = background color
        updates_per_sec = updates per second
        game = Game object
        """
        super(Engine, self).__init__()
        pygame.init()
        pygame.key.set_repeat(300, 50)
        if not pygame.font:
            exit()
        self.clock = pygame.time.Clock()
        self.updates_per_sec = kwargs.get('updates_per_sec', 50)
        width, height = kwargs.get('width', 640), kwargs.get('height', 480)
        self.pos = Rect(0, 0, width, height)
        self.screen = pygame.display.set_mode((width, height))
        self.caption = kwargs.get('caption', "Wind Engine.")
        pygame.display.set_caption(self.caption)

        self.game = kwargs.get('game', game.Game())
        self.game.setup(self)
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(kwargs.get('back_color', (0, 0, 0)))

        self.game.display()
        
    def add(self, child):
        self.contents = child
        self.contents.resize(*self.pos)
        
    def run(self):
        """Mainloop for catching events and performing updates."""
        while True:
            self.game.update()
            if self.contents:
                self.screen.blit(self.background, (0, 0))
                self.contents.display(self.screen)
            self.game.display()
            pygame.display.flip()
            self.clock.tick(self.updates_per_sec)
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                else:
                    self.game.handle_event(event)
                        
if __name__ == '__main__':
    Engine().run()
