#!/usr/bin/env python2

#
# Third example using the engine.
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
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 10, 30))
        self.container = Widget(width=640, height=240)
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
        self.screen.blit(self.background, (0, 0))
        self.container.display(self.screen)
        pygame.display.flip()

    def update(self):
        pass

    def handle_events(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        self.container.handle(event)
    
if __name__ == '__main__':
    e = Example()
    e.run()

