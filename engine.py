#!/usr/bin/env python2

#import ode
import pygame
from pygame.locals import *

class Engine(object):
    contents = None

    """Base engine for running the system."""
    def __init__(self, width=640, height=240):
        super(Engine, self).__init__()
        pygame.init()
        pygame.key.set_repeat(300, 50)
        if not pygame.font:
            exit()
        self.clock = pygame.time.Clock()
        self.updates_per_sec = 60
        self.pos = Rect(0, 0, width, height)
        self.screen = pygame.display.set_mode((width, height))
        self.caption = "Pygame Engine."
        pygame.display.set_caption(self.caption)
        self.setup()
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.display()
        
    def add(self, child):
        print child
        self.contents = child
        print self, child, self.contents
        self.contents.resize(*self.pos)
        
    def setup(self):
        """Run once at start up.
        Override this."""
        pass
        
    def display(self):
        """Run to display everything
        You can override this."""
        pass

    def update(self):
        """Run to update everything
        Override this."""
        pass

    def handle_events(self, event):
        """Callback for events
        Override this."""
        pass

    def run(self):
        """Mainloop for catching events and performing updates."""
        while True:
            self.update()
            if self.contents:
                self.screen.blit(self.background, (0, 0))
                self.contents.display(self.screen)
            self.display()
            pygame.display.flip()
            self.clock.tick(self.updates_per_sec)
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                else:
                    self.handle_events(event)
                        
if __name__ == '__main__':
    e = Engine()
    e.run()
