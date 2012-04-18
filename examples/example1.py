#!/usr/bin/env python2

#
# Simple example using the engine.
#

import pygame
from pygame.locals import *

import sys; sys.path.insert(0, '..')

from wind import *

class Example(Game):
    def setup(self, root):
        # Override some of the stuff in Engine
        self.caption = "Example."
        self.updates_per_sec = 30
        
        self.container = Widget(parent=root)
        self.textbox = Textbox("You can write here.",
                               width=320, height=100,
                               font_size=14,
                               color=(100, 200, 100),
                               parent=self.container)
        self.textbox2 = Textbox("Or here.",
                                width=320, height=100,
                                font_size=14,
                                color=(200, 100, 100),
                                parent=self.container)
        self.textbox3 = Textbox("Fllllloooow.",
                                width=320, height=100,
                                font_size=14,
                                color=(100, 100, 200),
                                parent=self.container,
                                read_only=True)
        self.textbox4 = Textbox("Sllllloooow.",
                                width=640,
                                height=20,
                                font_size=14,
                                color=(100, 200, 200),
                                parent=self.container,
                                read_only=True)

    def display(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        self.container.handle(event)
    
if __name__ == '__main__':
    Engine(width=640, height=240, back_color=(0,10,30), game=Example()).run()


