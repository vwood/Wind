import pygame
from pygame.locals import *
import sprite

class SpriteSheet(object):
    def __init__(self, image, **kwargs):
        """Create a new spritesheet.

        image = image file
        kwargs are name: tuple of (x, y, w, h).
        """
        self.image = pygame.image.load(image).convert_alpha()
        self.sprites = {}
        for key, value in kwargs.iteritems():
            self.sprites[key] = value

    def sprite(self, name):
        """Get a sprite from the sheet."""
        return sprite.Sprite(image=self.image,
                             image_pos = self.sprites[name])
