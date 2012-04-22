import pygame
from pygame.locals import *
import widget
from util import *

class Tabbedbox(widget.Widget):
    """A box that uses tabs to contain other widgets.
    
    width, height = size
    parent = parent widget
    font = pygame.font object to render text
    font_size = size of the font
    color = color of text and other foreground
    read_only = Boolean, is the textbox read only?
    
    """
    def __init__(self, **kwargs):
        super(Tabbedbox, self).__init__(**kwargs)

        self.tab_spacing = 4
        self.tab_height = self.font_size + self.tab_spacing
        self.tab_color = (120, 120, 200)
    
    # This has calculations that belong elsewhere
    # and should be placed elsewhere
    def display(self, surface):
        """Display the selected widget, and the tabs."""
        x, y, w, h = self.pos
        clip = surface.get_clip()
        surface.set_clip(self.pos)
        
        pygame.draw.line(surface, self.tab_color, (x, y + self.tab_height), (x + w, y + self.tab_height))

        current_x = x
        for i, item in enumerate(self.contents):
            this_w, _ = self.font.size(item.name)
            pygame.draw.line(surface, self.tab_color,
                             (x + current_x, y),
                             (x + current_x, y + self.tab_height))
            current_x += self.tab_spacing
            if item == self.selection:
                blit_text(surface, item.name, x + current_x, y, self.font, self.color)
            else:
                blit_text(surface, item.name, x + current_x, y, self.font, self.tab_color)
            current_x += this_w + self.tab_spacing

        if self.selection:
            _, _, s_w, s_h = self.selection.pos
            self.selection.resize(x, y + self.tab_height, min(s_w, w), min(s_h, h - self.tab_height))
            self.selection.display(surface)
            
        surface.set_clip(clip)

    def handle(self, event):
        """Handle pygame events.

        self.selection handles the event dispatch.
        Except for tab mouse events which change the current selection.
        (Or go to the selection if in that space.

        """
        if event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos
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
