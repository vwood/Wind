import pygame
from pygame.locals import *
import widget
from util import *

# TODO: Support an image rather than text...
class Button(widget.Widget):
    """A button that uses a callback."""
    def __init__(self, label="", callback = lambda: None, **kwargs):
        super(Button, self).__init__(**kwargs)

        self.padding = 4
        w, h = self.font.size(label)
        self.resize(w=w + self.padding * 2, h=h + self.padding * 2)

        self.back_color = (120, 120, 200)
        self.label = label
        self.callback = callback

    def display(self, surface):
        """Display the selected widget, and the tabs."""
        x, y, w, h = self.pos
        
        pygame.draw.rect(surface, self.back_color, Rect(x, y, w - 1, h - 1), 2)
        blit_text(surface, self.label, x + self.padding, y + self.padding, self.font, self.color)

    def handle(self, event):
        """self.selection handles the event dispatch.
        Except for tab mouse events which change the current selection.
        (Or go to the selection if in that space."""
        if event.type == MOUSEBUTTONDOWN:
            self.callback()
