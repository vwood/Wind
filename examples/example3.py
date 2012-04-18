#!/usr/bin/env python2

#
# Third example using the engine.
#

import pygame
from pygame.locals import *

import sys; sys.path.insert(0, '..')
if sys.version_info < (2, 7):
    from __init__ import *
else:
    from wind import *

class Example(Engine):
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
        self.button = Button(label="Quit",
                             callback=exit,
                             font_size=14,
                             parent=self.container)
        self.button2 = Button(image=pygame.image.load("resources/button_purple.png").convert_alpha(),
                              callback=exit,
                              padding=0,
                              parent=self.container)

    def display(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        self.container.handle(event)
    
if __name__ == '__main__':
    Engine(width=640, height=480, back_color=(0,30,10), game=Example()).run()
