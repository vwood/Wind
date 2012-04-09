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
        self.textbox = Textbox("You can write here.", 320, 100, 14, (100, 200, 100))
        self.textbox2 = Textbox("Or here.", 320, 100, 14, (200, 100, 100))
        self.textbox2.show_cursor = False
        self.textbox3 = Textbox("Fllllloooow.", 320, 100, 14, (100, 100, 200))
        self.textbox3.show_cursor = False
        self.button = Button("Quit", lambda: exit(), 14)

        self.container = Widget(640, 240)
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
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            else:
                self.textbox.handle_keydown(event)
    
if __name__ == '__main__':
    e = Example()
    e.run()
