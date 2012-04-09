import pygame
from pygame.locals import *
import widget
from util import *

class Tabbedbox(widget.Widget):
    """A box that uses tabs to contain other widgets."""
    def __init__(self, width=32, height=1, font_size=14):
        super(Tabbedbox, self).__init__()
        self.width, self.height = width, height
        self.font = pygame.font.Font("Inconsolata.otf", font_size)
        self.font_size = font_size
        self.tab_spacing = 4
        self.tab_height = font_size + self.tab_spacing
        self.back_color = (120, 120, 200)
        self.fore_color = (200, 120, 120)
    
    # This has calculations that belong elsewhere
    # and should be placed elsewhere
    def display(self, surface, x=0, y=0, w=None, h=None):
        """Display the selected widget, and the tabs."""
        if w == None: w = surface.get_width() - x
        if h == None: h = surface.get_height() - y
        
        pygame.draw.line(surface, self.back_color, (x, y + self.tab_height), (x + w, y + self.tab_height))

        current_x = x
        for i, item in enumerate(self.contents):
            this_w, _ = self.font.size(item.name)
            pygame.draw.line(surface, self.back_color,
                             (x + current_x, y),
                             (x + current_x, y + self.tab_height))
            current_x += self.tab_spacing
            if item == self.selection:
                blit_text(surface, item.name, x + current_x, y, self.font, self.fore_color)
            else:
                blit_text(surface, item.name, x + current_x, y, self.font, self.back_color)
            current_x += this_w + self.tab_spacing

        if self.selection:
            clip = surface.get_clip()
            surface.set_clip(Rect(x, y + self.tab_height,
                                  min(self.selection.width, w), min(self.selection.height, h - self.tab_height)))
            self.selection.display(surface, x, y + self.tab_height,
                                   min(item.width, w), min(item.height, h - self.tab_height))
            surface.set_clip(clip)

    def handle(self, event):
        """self.selection handles the event dispatch.
        Except for tab mouse events which change the current selection.
        (Or go to the selection if in that space."""
        if event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos
            print event.pos
            if my < self.tab_height:
                for tab in self.contents:
                    tab_width, _ = self.font.size(tab.name)
                    tab_width += self.tab_spacing * 2
                    if mx < tab_width:
                        self.selection = tab
                        break
                    mx -= tab_width
            else:
                self.selection.handle(event)
        elif event.type == KEYDOWN:
            if self.selection:
                self.selection.handle(event)
