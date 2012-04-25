import pygame
from pygame.locals import *
import sprite
import widget

class Entity(widget.Widget, sprite.Sprite):
    def __init__(self, **kwargs):
        """Create a new Entity.

        x, y = position
        width, height = size
        parent = parent widget, will add to the parent if specified.
        image = image filename or pygame surface
        image_pos = tuple of the position in the image, None (default) for entire image.

        """
        super(Sprite, self).__init__(**kwargs)

        self.image = kwargs.get('image', None)
        if type(self.image) is str:
            self.image = pygame.image.load(self.image).convert_alpha()
        iw, ih = self.image.get_size()
        self.image_pos = kwargs.get('image_pos', (0, 0, iw, ih))
        x, y = kwargs.get('x', 0), kwargs.get('y', 0)
        w, h = kwargs.get('width', iw), kwargs.get('height', ih)
        self.pos = Rect(x, y, w, h)

    def display(self, surface):
        """Display the sprite."""
        surface.blit(self.image, self.pos, self.image_pos)

    def move(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy
        
