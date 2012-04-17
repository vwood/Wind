#!/usr/bin/env python2

#import ode
import pygame
from pygame.locals import *

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
        self.setup()
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(kwargs.get('back_color', (0, 0, 0)))

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
