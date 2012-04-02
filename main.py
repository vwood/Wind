#!/usr/bin/env python2

#import ode
#from pgu import gui as pgui
import pygame
from pygame.locals import *

# TODO: I would prefer objects... with editable text.
# TODO: Store the font once in resource management (env)
# TODO: Store list of text, and only rerender when it changes
def blit_text(surface, text, x=None, y=None, size=12, color=(255, 255, 255)):
    """Display a string on a surface centred at x & y.
    If either of x or y are not set, the text is centred on that axis."""
    font = pygame.font.Font("Inconsolata.otf", size)
    text = font.render(text, True, color) # True for antialiasing
    if x == None:
        x = surface.get_width() / 2
    if y == None:
        y = surface.get_height() / 2
    pos = text.get_rect(x = x, y = y)
    surface.blit(text, pos)

class Rope(object):
    """Concatenation tree for strings."""
    def __init__(self):
        self.contents = []
        self.lengths = []

    def __str__(self):
        return "".join(self.contents)

class Widget(object):
    """A GUI item.
    May contain other GUI items."""
    def __init__(self):
        self.contents = []
        self.width, self.height = 1, 1
        self.selection = None

    def set_size(self, w, h):
        self.width, self.height = w, h

    def display(self, surface):
        pass

    def handle(self, event):
        """self.selection handles the event dispatch.
        Except for mouse events which go to whatever is clicked upon.
        Which then changes the current selection."""
        if event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == KEYDOWN:
            pass
    
# TODO: Start using editor.py
# TODO: Text selection    
# TODO: Line wrap + line maximums (can't just add \n's !)
# TODO: enforce width and height (screen location)
# TODO: Simple syntax highlighting (requires meta data)
# TODO: the contents should be held in a rope with speed up for going up and down lines...
# TODO: keybindings stored in a dict. (or several dicts.)
class TextBox(Widget):
    """A box that contains text."""
    def __init__(self, contents="", width=32, height=1, font_size=24, color=(255, 255, 255)):
        self.width, self.height = width, height
        self.contents = contents.split("\n")
        self.font_size = font_size
        self.char = 0
        self.line = 0
        self.color = color

    def display(self, surface, x, y):
        """Display the text box on a surface."""
        this_y = y
        for line in self.contents:
            blit_text(surface, line, x, this_y, self.font_size, self.color)
            this_y += self.font_size
        if pygame.time.get_ticks() / 500 % 2 == 0:
            font = pygame.font.Font("Inconsolata.otf", self.font_size)
            w, h = font.size(self.contents[self.line][:self.char])
            text = font.render(self.contents[self.line][:self.char], True, self.color)

            y = y + self.line * self.font_size
            pygame.draw.line(surface, self.color, (x+w, y), (x+w, y+h))

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
        
    def handle_event(self, event):
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
        self.textbox = TextBox("You can write here.", 0, 0, 14, (100, 200, 100))
        self.textbox2 = TextBox("Or here.", 0, 0, 14, (200, 100, 100))
#        self.gui = pgui.App()
#        container = pgui.Container()
#        container.add(pgui.TextArea("", 300, 200, 12), x=0, y=0)
#        container.add(pgui.TextArea("", 300, 200, 12), x=300, y=0)
#        self.gui.init(widget = container)
#        self.gui.run()
        self.display()

    def display(self):
        self.screen.blit(self.background, (0, 0))
        self.textbox.display(self.screen, 0, 0)
        self.textbox2.display(self.screen, 320, 0)
        pygame.display.flip()

    def run(self):
        """Mainloop for catching events and performing updates."""
        while True:
            self.display()
            self.clock.tick(60)
#            self.gui.loop()
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    else:
                        self.textbox.handle_event(event)
                        
if __name__ == '__main__':
    e = Engine()
    e.run()
