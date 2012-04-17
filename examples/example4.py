#!/usr/bin/env python2

#
# Fourth example using the engine.
#

import pygame
from pygame.locals import *

import sys; sys.path.insert(0, '..')

from wind import *

class Example(Engine):
    def setup(self):
        # Override some of the stuff in Engine
        self.caption = "Example."
        self.updates_per_sec = 30
        
        self.container = Widget(parent=self)
        self.textbox = Textbox("# python goes here.",
                               width=320, height=320,
                               parent=self.container,
                               font_size=14,
                               color=(140, 140, 200))
        self.canvas = Canvas(width=320, height=320,
                             parent=self.container)
        self.resultbox = Textbox("Result goes here.",
                                 width=640, height=32,
                                 font_size=14,
                                 read_only=True,
                                 parent=self.container)
        self.button = Button(label="run",
                             callback=exit,
                             parent=self.container)

    def display(self):
        pass

    def update(self):
        pass

    def handle_events(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        self.container.handle(event)
    
if __name__ == '__main__':
    e = Example(width=640, height=420)
    e.run()
