import pygame
from pygame.locals import *
import widget

class Canvas(widget.Widget):
    """A GUI canvas.
    Contains other items."""
    
    def __init__(self, **kwargs):
        """Create a new widget, options are:
        x, y = position
        width, height = size
        parent = parent widget, will add to the parent if specified.
        font = pygame.font object to render text
        font_size = size of the font
        color = color of text and other foreground
        """
        super(Canvas, self).__init__(**kwargs)        
        
    def add(self, child):
        if len(self.contents) == 0:
            self.selection = child
        child.parent = self
        self.contents.append(child)
        self.positions_are_dirty = True

    def remove(self, child):
        if self.selection == child:
            self.selection = None
        if child.parent == self:
            child.parent = None
        self.contents.remove(child)
        self.positions_are_dirty = True

    def display(self, surface):
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
