#!/usr/bin/env python2

#
# Fourth example using the engine.
#

import pygame
from pygame.locals import *

import sys; sys.path.insert(0, '..')
if sys.version_info < (2, 7):
    from __init__ import *
else:
    from wind import *

from StringIO import StringIO
    
class Example(Game):
    def setup(self, root):
        # Override some of the stuff in Engine
        self.caption = "Example."
        self.updates_per_sec = 30
        self.container = Widget(parent=root)
        self.textbox = Textbox("# python goes here.",
                               width=320, height=320,
                               parent=self.container,
                               font_size=14,
                               color=(140, 140, 200))
        self.canvas = Canvas(width=320, height=320,
                             parent=self.container)
        self.resultbox = Textbox("Result goes here.",
                                 width=320, height=32,
                                 font_size=14,
                                 read_only=True,
                                 parent=self.container)
        self.buttonbox = Textbox("Crap goes here.",
                                 width=320, height=32,
                                 font_size=14,
                                 read_only=True,
                                 parent=self.container)
        self.button = Button(label="run",
                             callback=self.push_button,
                             parent=self.container)
        self.pushes = 0

    def display(self):
        pass

    def update(self):
        pass

    def push_button(self):
        self.pushes += 1
        self.buttonbox.set_text("pushed button %d times." % (self.pushes,))

        buffer = StringIO()
        old_stdout = sys
        sys.stdout = buffer

        try:
            exec self.textbox.get_text()
            self.resultbox.set_text(buffer.getvalue())
        except Exception as e:
            self.resultbox.set_text(str(e))

        sys.stdout = old_stdout

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        self.container.handle(event)
    
if __name__ == '__main__':
    Engine(width=640, height=420, game=Example()).run()
