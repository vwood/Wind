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
        width, height = size
        parent = parent widget, will add to the parent if specified."""
        self.width, self.height = kwargs.get('width', 0), kwargs.get('height', 0)
        self.parent = kwargs.get('parent', None)
        if self.parent is not None:
            self.parent.add(self)

        self.selection = None

        self.contents = []
        self.contents_positions = []
        self.positions_are_dirty = False

    def resize(self, w, h):
        self.width, self.height = w, h
        self.positions_are_dirty = True

    def get_size(self):
        return (self.width, self.height)

    def add(self, child):
        if len(self.contents) == 0:
            self.selection = child
        self.contents.append(child)
        self.positions_are_dirty = True # TODO: perhaps just calculate the new items' position

    def calculate_positions(self, x, y, w, h):
        # Update if a child resizes
        if not self.positions_are_dirty: return

        current_x, current_y = 0, 0
        max_height_on_this_line = 0
        self.contents_positions = []
        for i,item in enumerate(self.contents):
            if item.width + current_x > w:
                current_y += max_height_on_this_line
                current_x = 0
                max_height_on_this_line = 0
            self.contents_positions.append(Rect(x + current_x, y + current_y,
                                                min(item.width, w), min(item.height, h - current_y)))
            current_x += item.width
            if item.height > max_height_on_this_line:
                max_height_on_this_line = item.height
            
    def display(self, surface, x=0, y=0, w=None, h=None):
        if w == None: w = surface.get_width() - x
        if h == None: h = surface.get_height() - y

        self.calculate_positions(x, y, w, h)
        
        for item, pos in zip(self.contents, self.contents_positions):
            x, y, w, h = pos
            clip = surface.get_clip()
            surface.set_clip(pos)
            item.display(surface, x, y, w, h)
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
