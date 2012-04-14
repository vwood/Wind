import pygame
from pygame.locals import *
import widget
from util import *

# TODO: Support an image rather than text...
class Button(widget.Widget):
    """A button that uses a callback."""
    def __init__(self, label="", callback = lambda: None, **kwargs):
        super(Button, self).__init__(kwargs)

        self.width, self.height = self.font.size(label)
        self.padding = 4
        self.width += self.padding * 2
        self.height += self.padding * 2
        self.back_color = (120, 120, 200)
        self.label = label
        self.callback = callback

    def display(self, surface, x=0, y=0, w=None, h=None):
        """Display the selected widget, and the tabs."""
        if w == None: w = surface.get_width() - x
        if h == None: h = surface.get_height() - y
        
        pygame.draw.rect(surface, self.back_color, Rect(x, y, w - 1, h - 1), 2)
        blit_text(surface, self.label, x + self.padding, y + self.padding, self.font, self.color)

    def handle(self, event):
        """self.selection handles the event dispatch.
        Except for tab mouse events which change the current selection.
        (Or go to the selection if in that space."""
        if event.type == MOUSEBUTTONDOWN:
            self.callback()
