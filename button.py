import pygame
from pygame.locals import *
import widget
from util import *

class Button(widget.Widget):
    """A button that uses a callback."""

    focusable = False
    
    def __init__(self,  **kwargs):
        """Create a new button, options are:
        x, y = position
        width, height = size (calculated from image or label)
        label = The label on a text button (the default)
        font = pygame.font object to render text
        font_size = size of the font
        color = color of text and other foreground
        image = The image to place on an image button. (pygame surface)
        callback = A function of no arguments that is called when the button is pressed.
        padding = Padding around the text or image, set to 0 to have no border
        """
        super(Button, self).__init__(**kwargs)

        self.padding = kwargs.get('padding', 4)
        self.callback = kwargs.get('callback', lambda: None)

        self.image = kwargs.get('image', None)
        self.label = kwargs.get('label', "")

        if self.image:
            self.is_text_button = False
            w, h = self.image.get_size()
            self.resize(w=w + self.padding * 2, h=h + self.padding * 2)
        else:
            self.is_text_button = True
            w, h = self.font.size(self.label)
            self.resize(w=w + self.padding * 2, h=h + self.padding * 2)

        self.back_color = (120, 120, 200)

    def display(self, surface):
        """Display the selected widget, and the tabs."""
        x, y, w, h = self.pos

        if self.padding > 0:
            pygame.draw.rect(surface, self.back_color, Rect(x, y, w - 1, h - 1), 2)
        
        if self.is_text_button:
            blit_text(surface, self.label, x + self.padding, y + self.padding, self.font, self.color)
        else:
            surface.blit(self.image, (x + self.padding, y + self.padding))

    def handle(self, event):
        """self.selection handles the event dispatch.
        Except for tab mouse events which change the current selection.
        (Or go to the selection if in that space."""
        if event.type == MOUSEBUTTONDOWN:
            self.callback()
