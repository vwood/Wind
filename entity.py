import pygame
from pygame.locals import *
import sprite
import widget

class Entity(widget.Widget):
    def __init__(self, **kwargs):
        """Create a new Entity.

        x, y = position
        width, height = size
        parent = parent widget, will add to the parent if specified.
        sprite = sprite

        """
        super(Entity, self).__init__(**kwargs)

        self.sprite = kwargs.get('sprite', None)
        x, y = kwargs.get('x', 0), kwargs.get('y', 0)
        iw, ih = self.sprite.get_size()
        w, h = kwargs.get('width', iw), kwargs.get('height', ih)
        self.pos = Rect(x, y, w, h)

    def display(self, surface):
        """Display the sprite."""
        self.sprite.display(surface, self.pos)

    def move(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy
        
    def update(self):
        pass
