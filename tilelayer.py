import pygame
from pygame.locals import *
import widget

class TileLayer(widget.Widget):
    def __init__(self, **kwargs):
        """Create a new Tilelayer.

        x, y = position
        width, height = size tile layer
        parent = parent widget, will add to the parent if specified.
        tile_width, tile_height = size of single tile
        tiles = list of tilenames
        spritesheet = spritesheet containing tilenames as sprites

        """
        super(TileLayer, self).__init__(**kwargs)

        x, y = kwargs.get('x', 0), kwargs.get('y', 0)
        w, h = kwargs.get('width', 32), kwargs.get('height', 32)
        self.pos = Rect(x, y, w, h)
        tw, th = (kwargs.get('tile_width', 16), kwargs.get('tile_height', 16))
        self.tile_size = (tw, th)
        self.tiles_across = w / tw
        self.tiles_down = h / th
        self.spritesheet = kwargs.get('spritesheet')
        self.tiles = [self.spritesheet.sprite(tilename) for tilename in kwargs.get('tiles', [])]
        self.layer = [[self.tiles[0] for _ in range(self.tiles_across)]
                      for _ in range(self.tiles_down)]
        
    def collide(self, sprite):
        x, y, _, _ = self.pos
        sx, sy, sw, sh = sprite.pos
        tw, th = self.tile_size
        return False
    
    def display(self, surface):
        """Display the tiles."""
        x, y, _, _ = self.pos
        tw, th = self.tile_size
        tile_pos = Rect(0, 0, tw, th)
        for i, row in enumerate(self.layer):
            for j, tile in enumerate(row):
                tile_pos.x = x + i * tw
                tile_pos.y = y + j * th
                tile_image, tile_image_pos = tile.image, tile.image_pos
                surface.blit(tile_image, tile_pos, tile_image_pos)
