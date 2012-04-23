#!/usr/bin/env python2

#
# Fifth example using the engine.
#

import pygame
from pygame.locals import *

import sys; sys.path.insert(0, '..')
if sys.version_info < (2, 7):
    from __init__ import *
else:
    from wind import *

class Example(Game):
    def setup(self, root):
        self.canvas = Canvas(width=640, height=420,
                             parent=root)
        self.mariosheet = SpriteSheet("resources/mario.gif",
                                      mario=(0,0,24,32))
        self.tilesheet = SpriteSheet("resources/platform.png",
                                      platform=(1,1,32,32))
        self.sprite = self.mariosheet.sprite("mario", 340, 0, self.canvas)
        self.tile = self.tilesheet.sprite("platform", 300, 100, self.canvas)

    def display(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        self.canvas.handle(event)
    
if __name__ == '__main__':
    Engine(caption="Example Five.",
           updates_per_sec=30,
           width=640, height=420,
           game=Example()).run()
