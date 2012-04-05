#!/usr/bin/env python

#import ode
import pygame
from pygame.locals import *

# TODO: I would prefer objects... with editable text.
# TODO: Store the font once in resource management (env)
# TODO: Store list of text, and only rerender when it changes
def blit_text(surface, text, x, y, size=12, color=(255, 255, 255)):
    """Display a string on a surface centred at x & y."""
    font = pygame.font.Font("Inconsolata.otf", size)
    text = font.render(text, True, color) # True for antialiasing
    pos = text.get_rect(x = x, y = y)
    surface.blit(text, pos)

class Rope(object):
    """Concatenation tree for strings."""
    def __init__(self):
        self.contents = []
        self.lengths = []

    def __str__(self):
        return "".join(self.contents)

# TODO: create a tabbed selection widget
class Widget(object):
    """A GUI item.
    May contain other GUI items. (in a flow based layout)"""
    def __init__(self, width=1, height=1):
        self.contents = []
        self.width, self.height = width, height
        self.selection = None

    def set_size(self, w, h):
        self.width, self.height = w, h

    def get_size(self):
        return (self.width, self.height)

    def add(self, child):
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
                item.display(surface,
                             x + current_x, y + current_y,
                             min(item.width, w), min(item.height, h - current_y))
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

# TODO: Start using editor.py
# TODO: Text selection    
# TODO: Line wrap + line maximums (can't just add \n's !)
# TODO: Simple syntax highlighting (requires meta data)
# TODO: the contents should be held in a rope with speed up for going up and down lines...
# TODO: keybindings stored in a dict. (or several dicts.)

# TODO: enforce width and height (screen location)
# TODO: scroll with wheel mouse
# TODO: show current view on the side
class TextBox(Widget):
    """A box that contains text."""
    def __init__(self, contents="", width=32, height=1, font_size=24, color=(255, 255, 255)):
        super(TextBox, self).__init__()
        self.width, self.height = width, height
        self.contents = contents.split("\n")
        self.font_size = font_size
        self.char = 0
        self.line = 0
        self.color = color
        self.show_cursor = True
        
    def display(self, surface, x, y, w=None, h=None):
        """Display the text box on a surface."""
        font = pygame.font.Font("Inconsolata.otf", self.font_size)
        
        line_breaks = 0
        for i, line in enumerate(self.contents):
            if self.show_cursor and i == self.line and pygame.time.get_ticks() / 500 % 2 == 0:
                w, h = font.size(self.contents[self.line][:self.char])
                pygame.draw.line(surface, self.color, (x+w, y), (x+w, y+h))
            blit_text(surface, line, x, y, self.font_size, self.color)
            y += self.font_size
            
    def insert(self, s):
        """Insert a string at the cursor (as if it were typed)."""
        self.contents[self.line] = (self.contents[self.line][:self.char]
                                    + s
                                    + self.contents[self.line][self.char:])
        self.char += len(s)

    def insert_newline(self):
        """Insert a newline at the cursor (as if it were typed)."""
        self.contents = (self.contents[:self.line]
                         + [self.contents[self.line][:self.char],
                            self.contents[self.line][self.char:]]
                         + self.contents[self.line + 1:])
        self.line += 1
        self.char = 0

    def cursor_up(self):
        if self.line > 0:
            self.line -= 1

    def cursor_left(self):
        if self.char > 0:
            self.char -= 1
        elif self.line > 0:
            self.line -= 1
            self.char = len(self.contents[self.line])

    def cursor_right(self):
        if self.char <= len(self.contents[self.line]):
            self.char += 1
        elif self.line < len(self.contents) - 1:
            self.char = 0
            self.line += 1

    def cursor_down(self):
        if self.line < len(self.contents) - 1:
            self.line += 1

    def delete_char_backwards(self):
        if self.char > 0:
            self.contents[self.line] = (self.contents[self.line][:self.char - 1]
                                        + self.contents[self.line][self.char:])
            self.char -= 1
        elif self.line > 0:
            self.char = len(self.contents[self.line - 1])
            self.contents = (self.contents[:self.line - 1]
                             + [self.contents[self.line - 1]
                                + self.contents[self.line]]
                             + self.contents[self.line + 1:])
            self.line -= 1

    def delete_char_forwards(self):
        if self.char < len(self.contents[self.line]):
            self.contents[self.line] = (self.contents[self.line][:self.char]
                                        + self.contents[self.line][self.char + 1:])
        elif self.line < len(self.contents) - 1:
            self.contents = (self.contents[:self.line]
                             + [self.contents[self.line]
                                + self.contents[self.line + 1]]
                             + self.contents[self.line + 2:])

    def delete_til_end_of_line(self):
        if self.char < len(self.contents[self.line]):
            self.contents[self.line] = self.contents[self.line][:self.char]
        elif self.line < len(self.contents) - 1:
            self.contents = (self.contents[:self.line]
                             + [self.contents[self.line]
                                + self.contents[self.line + 1]]
                             + self.contents[self.line + 2:])
        
    def cursor_start_of_line(self):
        self.char = 0

    def cursor_end_of_line(self):
        self.char = len(self.contents[self.line])

    def handle(self, event):
        """Overrides the widget method."""
        if event.type == KEYDOWN:
            self.handle_keydown(event)
        
    def handle_keydown(self, event):
        """Handles keydown events given to the TextBox."""
        if event.key == K_RETURN:
            self.insert_newline()
        elif event.key == K_TAB:
            self.insert(' ' * 4)
        elif event.key == K_UP:
            self.cursor_up()
        elif event.key == K_LEFT:
            self.cursor_left()
        elif event.key == K_RIGHT:
            self.cursor_right()
        elif event.key == K_DOWN:
            self.cursor_down()
        elif event.key == K_BACKSPACE:
            self.delete_char_backwards()
        elif event.key == K_DELETE:
            self.delete_char_forwards()
        elif event.mod & KMOD_CTRL:
            if event.key == ord('a'):
                self.cursor_start_of_line()
            elif event.key == ord('d'):
                self.delete_char_forwards()
            elif event.key == ord('k'):
                self.delete_til_end_of_line()
            elif event.key == ord('e'):
                self.cursor_end_of_line()
            elif event.key == ord('n'):
                self.cursor_down()
            elif event.key == ord('p'):
                self.cursor_up()
            elif event.key == ord('b'):
                self.cursor_left()
            elif event.key == ord('f'):
                self.cursor_right()
        else:
            self.insert(event.unicode)
    
class Engine(object):
    """Base engine for running the system."""
    def __init__(self, width=640, height=240):
        super(Engine, self).__init__()
        pygame.init()
        pygame.key.set_repeat(300, 50)
        if not pygame.font:
            exit()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Engine")
        self.clock = pygame.time.Clock()
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 10, 30))
        self.textbox = TextBox("You can write here.", 320, 100, 14, (100, 200, 100))
        self.textbox2 = TextBox("Or here.", 320, 100, 14, (200, 100, 100))
        self.textbox2.show_cursor = False
        self.textbox3 = TextBox("Fllllloooow.", 320, 100, 14, (100, 100, 200))
        self.textbox3.show_cursor = False

        self.container = Widget(640, 240)
        self.container.add(self.textbox)
        self.container.add(self.textbox2)
        self.container.add(self.textbox3)
        self.display()

    def display(self):
        self.screen.blit(self.background, (0, 0))
        self.container.display(self.screen)
        pygame.display.flip()

    def run(self):
        """Mainloop for catching events and performing updates."""
        while True:
            self.display()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    else:
                        self.textbox.handle_keydown(event)
                        
if __name__ == '__main__':
    e = Engine()
    e.run()
