#!/usr/bin/env python

#import ode
#from pgu import gui as pgui
import pygame
from pygame.locals import *

# TODO: I would prefer objects... with editable text.
def blit_text(surface, text, x=None, y=None, size=12, color=(255, 255, 255)):
    """Display a string on a surface centred at x & y.
    If either of x or y are not set, the text is centred on that axis."""
    font = pygame.font.Font("Inconsolata.otf", size) # Fonts should be stored in some form of resource management (env)
    text = font.render(text, True, color) # True for antialiasing
    if x == None:
        x = surface.get_width() / 2
    if y == None:
        y = surface.get_height() / 2
    pos = text.get_rect(x = x, y = y)
    surface.blit(text, pos)


# TODO: Needs key repeating (on hold)
# TODO: Text selection    
# TODO: Line wrap + line maximums (can't just add \n's !)
# TODO: Simple syntax highlighting
class TextBox(object):
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

    def handle_event(self, event):
        if event.key == K_RETURN:
            self.contents = (self.contents[:self.line]
                             + [self.contents[self.line][:self.char],
                                self.contents[self.line][self.char:]]
                             + self.contents[self.line + 1:])
            self.line += 1
            self.char = 0
        elif event.key == K_TAB:
            self.insert(' ' * 4)
        elif event.key == K_UP:
            if self.line > 0: self.line -= 1
        elif event.key == K_LEFT:
            if self.char > 0:
                self.char -= 1
            elif self.line > 0:
                self.line -= 1
                self.char = len(self.contents[self.line])
        elif event.key == K_RIGHT:
            if self.char <= len(self.contents[self.line]):
                self.char += 1
            elif self.line < len(self.contents) - 1:
                self.char = 0
                self.line += 1
        elif event.key == K_DOWN:
            if self.line < len(self.contents) - 1: self.line += 1
        elif event.key == K_BACKSPACE:
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
        elif event.key == K_DELETE:
            if self.char < len(self.contents[self.line]):
                self.contents[self.line] = (self.contents[self.line][:self.char]
                                 + self.contents[self.line][self.char + 1:])
            elif self.line < len(self.contents) - 1:
                self.contents = (self.contents[:self.line]
                                 + [self.contents[self.line]
                                    + self.contents[self.line + 1]]
                                 + self.contents[self.line + 2:])
        else:
            self.insert(event.unicode)
    
class Engine(object):
    """Base engine for running the system."""
    def __init__(self, width=640, height=240):
        super(Engine, self).__init__()
        pygame.init()
        if not pygame.font:
            exit()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Engine")
        self.clock = pygame.time.Clock()
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 10, 30))
        self.textbox = TextBox("Default")
#        self.gui = pgui.App()
#        container = pgui.Container()
#        container.add(pgui.TextArea("", 300, 200, 12), x=0, y=0)
#        container.add(pgui.TextArea("", 300, 200, 12), x=300, y=0)
#        self.gui.init(widget = container)
#        self.gui.run()
        self.display()

    def display(self):
        self.screen.blit(self.background, (0, 0))
        self.textbox.display(self.screen, 80, 80)
        blit_text(self.screen, "Test\nText", 20, 20, 20, (200,200,200))
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

