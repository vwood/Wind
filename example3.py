#!/usr/bin/env python2

#
# Third example using the engine.
#

import pygame
from pygame.locals import *
from wind import *

class Example(Engine):
    def setup(self):
        # Override some of the stuff in Engine
        self.caption = "Example."
        self.updates_per_sec = 30
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 10, 30))
        self.textbox = Textbox("You can write here.", width=320, height=100, font_size=14, color=(100, 200, 100))
        self.textbox2 = Textbox("Or here.", width=320, height=100, font_size=14, color=(200, 100, 100))
        self.textbox3 = Textbox("Fllllloooow.", width=320, height=100, font_size=14, color=(100, 100, 200), read_only=True)
        self.button = Button("Quit", exit, 14)

        self.container = Widget(width=640, height=240)
        self.container.add(self.textbox)
        self.container.add(self.textbox2)
        self.container.add(self.textbox3)
        self.container.add(self.button)

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

