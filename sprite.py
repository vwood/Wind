import pygame
from pygame.locals import *
import widget

class Sprite(widget.Widget):
    def __init__(self, **kwargs):
        """Create a new Sprite.

        x, y = position
        width, height = size
        parent = parent widget, will add to the parent if specified.
        image = image filename.

        """
