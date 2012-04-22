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
        self.container = Widget(parent=root)
        self.textbox = Textbox(content="# python goes here.\nprint \"hello, world!\"",
                               width=320, height=320,
                               parent=self.container,
                               font_size=14,
                               color=(140, 140, 200))
        self.canvas = Canvas(width=320, height=320,
                             parent=self.container)
        self.resultbox = Textbox(content="Result goes here.",
                                 width=640, height=64,
                                 font_size=14,
                                 read_only=True,
                                 parent=self.container)
        self.button = Button(label="run",
                             callback=self.push_button,
                             parent=self.container)
        Widget(width=16, parent=self.container) # Spacing

    def display(self):
        pass

    def update(self):
        pass

    def push_button(self):
        buffer = StringIO()
        old_stdout = sys
        sys.stdout = buffer

        try:
            result = eval(self.textbox.get_text())
            self.resultbox.set_text(str(result))
            return
        except SyntaxError:
            pass
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
    Engine(caption="Example Four.",
           updates_per_sec=30,
           width=640, height=420,
           game=Example()).run()
