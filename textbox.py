import pygame
import widget
from util import *

# TODO: Start using editor.py
# TODO: Text selection    
# TODO: Line wrap + line maximums (can't just add \n's !)
# TODO: Simple syntax highlighting (requires meta data)
# TODO: the contents should be held in a rope with speed up for going up and down lines...
# TODO: keybindings stored in a dict. (or several dicts.)

# TODO: enforce width and height (screen location)
# TODO: scroll with wheel mouse
# TODO: show current view on the side
class Textbox(widget.Widget):
    """A box that contains text."""

    def __init__(self, contents = "", **kwargs):
        """Create a new textbox,
        contents = initial contents
        
        keyword options are:
        
        width, height = size
        parent = parent widget
        font = pygame.font object to render text
        font_size = size of the font
        color = color of text and other foreground
        read_only = Boolean, is the textbox read only?
        """

        super(Textbox, self).__init__(**kwargs)

        self.contents = contents.split('\n')

        self.read_only = kwargs.get('read_only', False)
        self.point = len(self.contents)
        self.scroll = 0
        
    def display(self, surface):
        """Display the text box on a surface."""
        x, y, _, _ = self.pos

        point_line = self.point_line()
        self.skipped_lines = 0
        for i, line in enumerate(self.contents[self.scroll:]):
            i += self.scroll
            if not self.read_only and i == point_line and pygame.time.get_ticks() / 500 % 2 == 0:
                w, h = self.font.size(self.contents[point_line][:self.point])
                pygame.draw.line(surface, self.color, (x+w, y), (x+w, y+h))
            blit_text(surface, line, x, y, self.font, self.color)
            y += self.font_size

    def point_line(self, point=None):
        """Returns the line on which the point is."""
        if point is None: point = self.point
            
        total_len = 0
        for i, line in enumerate(self.contents):
            total_len += len(line)
            if self.point <= total_len:
                return i
        return total_len
        
    # EDITOR COMMANDS
    def insert(self, s):
        """Insert a string at the cursor (as if it were typed)."""
        if self.read_only: return
        self.contents[self.line] = (self.contents[self.line][:self.char]
                                    + s
                                    + self.contents[self.line][self.char:])
        self.char += len(s)

    def insert_newline(self):
        """Insert a newline at the cursor (as if it were typed)."""
        if self.read_only: return
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
        if self.read_only: return
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
        if self.read_only: return
        if self.char < len(self.contents[self.line]):
            self.contents[self.line] = (self.contents[self.line][:self.char]
                                        + self.contents[self.line][self.char + 1:])
        elif self.line < len(self.contents) - 1:
            self.contents = (self.contents[:self.line]
                             + [self.contents[self.line]
                                + self.contents[self.line + 1]]
                             + self.contents[self.line + 2:])

    def delete_til_end_of_line(self):
        if self.read_only: return
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

    def scroll_up(self):
        if self.scroll > 0:
            self.scroll -= 1
        
    def scroll_down(self):
        # TODO: bounds checking here
        self.scroll += 1

    # Event Handling
    def handle(self, event):
        """Overrides the widget method."""
        if event.type == KEYDOWN:
            self.handle_keydown(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4: # Scroll wheel up
                self.scroll_up()
            elif event.button == 5: # Scroll wheel down
                self.scroll_down()
            
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
