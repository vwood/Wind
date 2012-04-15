import pygame
from pygame.locals import *

# TODO: go from data structures to GUI
# TODO: create a proxy surface/view handler
# TODO: Split out the flow-based container stuck inside here
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
        self.set_parent(kwargs.get('parent', None))
        
        self.font_size = kwargs.get('font_size', 16)
        if kwargs.has_key('font'):
            self.font = kwargs['font']
        else:
            self.font = pygame.font.Font("resources/Inconsolata.otf", self.font_size)
        self.color = kwargs.get('color', (255, 255, 255))
        
        self.selection = None

        self.contents = []
        self.positions_are_dirty = False

    def resize(self, x=None, y=None, w=None, h=None):
        if x is None: x, _, _, _ = self.pos
        if y is None: _, y, _, _ = self.pos
        if w is None: _, _, w, _ = self.pos
        if h is None: _, _, _, h = self.pos
        self.pos = Rect(x, y, w, h)
        self.positions_are_dirty = True

    def get_rect(self):
        return self.pos

    def set_parent(self, new_parent):
        if self.parent == new_parent:
            return
        if self.parent:
            self.parent.remove(self)
        self.parent = new_parent
        if new_parent:
            self.parent.add(self)
    
    def add(self, child):
        if len(self.contents) == 0:
            self.selection = child
        child.parent = self
        self.contents.append(child)
        self.positions_are_dirty = True # TODO: perhaps just calculate the new items' position

    def remove(self, child):
        if self.selection == child:
            self.selection = None
        if child.parent == self:
            child.parent = None
        self.contents.remove(child)
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
            item.resize(x + current_x, y + current_y, min(iw, w), min(ih, h - current_y))
            current_x += iw
            if ih > max_height_on_this_line:
                max_height_on_this_line = ih
            
    def display(self, surface):
        self.calculate_positions()
        clip = surface.get_clip()
        surface.set_clip(self.pos)
        for item in self.contents:
            item.display(surface)
        surface.set_clip(clip)

    def handle(self, event):
        """self.selection handles the event dispatch.
        Except for mouse events which go to whatever is clicked upon.
        Which then changes the current selection."""
        if event.type == MOUSEBUTTONDOWN:
            for item in self.contents:
                if item.get_rect().collidepoint(event.pos):
                    self.selection = item
                    item.handle(event)
                    return
        elif event.type == KEYDOWN:
            if self.selection:
                self.selection.handle(event)
