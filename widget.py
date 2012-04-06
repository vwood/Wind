import pygame
from pygame.locals import *

# TODO: make resizable bit - resize to fit certain windows.
# TODO: create a proxy surface/view handler
# TODO: create a tabbed selection widget
# TODO: Widgets should be resized to fit the available space.
class Widget(object):
    """A GUI item.
    May contain other GUI items. (in a flow based layout)"""
    def __init__(self, width=1, height=1):
        self.contents = []
        self.width, self.height = width, height
        self.selection = None
        self.name = "Unnamed"

    def resize(self, w, h):
        self.width, self.height = w, h

    def get_size(self):
        return (self.width, self.height)

    def add(self, child):
        if len(self.contents) == 0:
            self.selection = child
        self.contents.append(child)

    def display(self, surface, x=0, y=0, w=None, h=None):
        """TODO: Calculate positions only if they ever change!
        Store them for calls like MOUSEBUTTONDOWN..."""
        if w == None: w = surface.get_width() - x
        if h == None: h = surface.get_height() - y
        
        current_y = 0
        current_x = 0
        max_height_on_this_line = 0
        for item in self.contents:
            if item.width + current_x <= w:
                clip = surface.get_clip()
                surface.set_clip(Rect(x + current_x, y + current_y, min(item.width, w), min(item.height, h - current_y)))
                item.display(surface,
                             x + current_x, y + current_y,
                             min(item.width, w), min(item.height, h - current_y))
                surface.set_clip(clip)
                current_x += item.width
                if item.height > max_height_on_this_line:
                    max_height_on_this_line = item.height
            else:
                # Display on next line (this will be same line, at the start)
                current_y += max_height_on_this_line
                item.display(surface,
                             x, y + current_y,
                             min(item.width, w), min(item.height, h - current_y))
                current_x = item.width
                max_height_on_this_line = item.height
                
    def handle(self, event):
        """self.selection handles the event dispatch.
        Except for mouse events which go to whatever is clicked upon.
        Which then changes the current selection."""
        if event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == KEYDOWN:
            if self.selection:
                self.selection.handle(event)
