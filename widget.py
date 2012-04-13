import pygame
from pygame.locals import *

# TODO: go from data structures to GUI
# TODO: make resizable bit - resize to fit certain windows.
# TODO: create a proxy surface/view handler
# TODO: Widgets should be resized to fit the available space.
class Widget(object):
    """A GUI item.
    May contain other GUI items. (in a flow based layout)"""

    name = "Unnamed"
    parent = None
    
    def __init__(self, **kwargs):
        """Create a new widget, options are:
        x, y = position
        width, height = size
        parent = parent widget, will add to the parent if specified.
        font = pygame.font object to render text
        font_size = size of the font
        color = color of text and other foreground
        """
        
        self.pos = Rect(kwargs.get('x', 0), kwargs.get('y', 0),
                        kwargs.get('width', 0), kwargs.get('height', 0))
        self.parent = kwargs.get('parent', None)
        if self.parent is not None:
            self.parent.add(self)

        self.font_size = kwargs.get('font_size', 16)
        if kwargs.has_key('font'):
            self.font = kwargs['font']
        else:
            self.font = pygame.font.Font("Inconsolata.otf", self.font_size)
        self.color = kwargs.get('color', (255, 255, 255))
        
        self.selection = None

        self.contents = []
        self.contents_positions = []
        self.positions_are_dirty = False

    def resize(self, w, h):
        x, y, _, _ = self.pos
        self.pos = Rect(x, y, w, h)
        self.positions_are_dirty = True

    def get_size(self):
        _, _, w, h = self.pos
        return (w, h)

    def add(self, child):
        if len(self.contents) == 0:
            self.selection = child
        self.contents.append(child)
        self.positions_are_dirty = True # TODO: perhaps just calculate the new items' position

    def calculate_positions(self):
        # Update if a child resizes
        if not self.positions_are_dirty: return

        x, y, w, h = self.pos
        current_x, current_y = 0, 0
        max_height_on_this_line = 0
        self.contents_positions = []
        for i,item in enumerate(self.contents):
            ix, iy, iw, ih = item.pos
            if iw + current_x > w:
                current_y += max_height_on_this_line
                current_x = 0
                max_height_on_this_line = 0
            self.contents_positions.append(Rect(x + current_x, y + current_y,
                                                min(iw, w), min(ih, h - current_y)))
            current_x += iw
            if ih > max_height_on_this_line:
                max_height_on_this_line = ih
            
    def display(self, surface):
        x, y, w, h = self.pos

        self.calculate_positions()
        
        for item, pos in zip(self.contents, self.contents_positions):
            x, y, w, h = pos
            clip = surface.get_clip()
            surface.set_clip(pos)
            item.display(surface)
            surface.set_clip(clip)

    def handle(self, event):
        """self.selection handles the event dispatch.
        Except for mouse events which go to whatever is clicked upon.
        Which then changes the current selection."""
        if event.type == MOUSEBUTTONDOWN:
            for i, pos in enumerate(self.contents_positions):
                if pos.collidepoint(event.pos):
                    self.selection = self.contents[i]
                    self.contents[i].handle(event)
                    return
        elif event.type == KEYDOWN:
            if self.selection:
                self.selection.handle(event)
