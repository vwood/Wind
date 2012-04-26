import pygame
from pygame.locals import *
import widget

class Sprite(object):
    def __init__(self, **kwargs):
        """Create a new Sprite.

        x, y = x, y offset
        width, height = size
        parent = parent widget, will add to the parent if specified.
        image = image filename or pygame surface
        image_pos = tuple of the position in the image, None (default) for entire image.

        """
        self.image = kwargs.get('image', None)
        if type(self.image) is str:
            self.image = pygame.image.load(self.image).convert_alpha()
        iw, ih = self.image.get_size()
        self.image_pos = kwargs.get('image_pos', (0, 0, iw, ih))
        self.x, self.y = kwargs.get('x', 0), kwargs.get('y', 0)

    def display(self, surface, pos):
        """Display the sprite."""
        x, y, _, _ = pos
        surface.blit(self.image, (x + self.x, y + self.y), self.image_pos)

    def get_size(self):
        _, _, iw, ih = self.image_pos
        return (iw, ih)
