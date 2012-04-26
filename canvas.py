import pygame
from pygame.locals import *
import widget

class Canvas(widget.Widget):
    """A GUI canvas.
    
    Contains other items.

    """
    
    def __init__(self, **kwargs):
        """Create a new Canvas widget.

        x, y = position
        width, height = size
        parent = parent widget, will add to the parent if specified.
        font = pygame.font object to render text.
        font_size = size of the font.
        color = color of text and other foreground.
        handler = an event handler that takes a pygame event.

        """
        super(Canvas, self).__init__(**kwargs)        

        self.event_handler = kwargs.get('handler', lambda event: None)
        
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
        """Handle pygame events.
        
        Canvases give the event to the underlying callback.

        """
        if event.type == MOUSEBUTTONDOWN:
            for item in self.contents:
                if item.get_rect().collidepoint(event.pos):
                    self.selection = item
                    item.handle(event)
                    return
        elif self.selection:
            self.selection.handle(event)
