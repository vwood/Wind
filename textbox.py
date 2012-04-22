import pygame
import widget
from util import *

class Textbox(widget.Widget):
    """A box that contains text."""

    def __init__(self, **kwargs):
        """Create a new textbox.
        
        content = initial contents
        width, height = size
        parent = parent widget
        font = pygame.font object to render text
        font_size = size of the font
        color = color of text and other foreground
        read_only = Boolean, is the textbox read only?
        
        """

        super(Textbox, self).__init__(**kwargs)

        contents = kwargs.get('content', '')
        self.contents = contents.split('\n')
        self.clipboard = ''
        
        self.point = len(contents) - 1
        self.line = self.point_line()        # Cached answer to point_line() queries

        self.read_only = kwargs.get('read_only', False)
        if self.read_only:
            self.focusable = False

        self.scroll = 0

        self.bindings = {K_RETURN: self.insert_newline, 
                         K_TAB: lambda: self.insert(self, ' ' * 4),
                         K_UP: self.cursor_up,
                         K_LEFT: self.cursor_left,
                         K_RIGHT: self.cursor_right,
                         K_DOWN: self.cursor_down,
                         K_BACKSPACE: self.delete_char_backwards,
                         K_DELETE: self.delete_char_forwards,
                         (KMOD_CTRL, ord('a')): self.cursor_start_of_line,
                         (KMOD_CTRL, ord('d')): self.delete_char_forwards,
                         (KMOD_CTRL, ord('k')): self.delete_til_end_of_line,
                         (KMOD_CTRL, ord('y')): self.yank,
                         (KMOD_CTRL, ord('e')): self.cursor_end_of_line,
                         (KMOD_CTRL, ord('n')): self.cursor_down,
                         (KMOD_CTRL, ord('p')): self.cursor_up,
                         (KMOD_CTRL, ord('b')): self.cursor_left,
                         (KMOD_CTRL, ord('f')): self.cursor_right,
                         (KMOD_CTRL, ord('l')): self.scroll_to_point}
        
    def display(self, surface):
        """Display the text box on a surface."""
        clip = surface.get_clip()
        surface.set_clip(self.pos)

        x, y, w, h = self.pos
        current_y = y
        self.skipped_lines = 0
        for i, line in enumerate(self.contents[self.scroll:]):
            i += self.scroll
            if not self.read_only and i == self.line and pygame.time.get_ticks() / 500 % 2 == 0:
                lw, lh = self.font.size(self.contents[self.line][:self.point])
                pygame.draw.line(surface, self.color, (x+lw, current_y), (x+lw, current_y+lh))
            blit_text(surface, line, x, current_y, self.font, self.color)
            current_y += self.font_size
            if current_y + self.font_size > y+h:
                break

        if i - self.scroll < len(self.contents) - 1:
            start_y = h * self.scroll / len(self.contents)
            end_y = h * (i + 1) / len(self.contents)
            pygame.draw.line(surface, self.color, (x+w-2, y+start_y), (x+w-2, y+end_y))
        surface.set_clip(clip)

    def point_line(self, point=None):
        """Returns the line on which the point is."""
        if point is None: point = self.point
            
        total_len = 0
        for i, line in enumerate(self.contents):
            total_len += len(line)
            if self.point <= total_len:
                return i
        return total_len

    def set_text(self, string):
        self.contents = string.split('\n')
        self.point = len(self.contents)
        self.line = self.point_line()

    def get_text(self):
        return "\n".join(self.contents)
    
    # EDITOR COMMANDS
    def insert_no_newlines(self, s):
        """Insert a string without newlines at the cursor (as if it were typed)."""
        if self.read_only: return
        self.contents[self.line] = (self.contents[self.line][:self.point]
                                    + s
                                    + self.contents[self.line][self.point:])
        self.point += len(s)

    def insert(self, s):
        """Insert a string at the cursor (as if it were typed)."""
        if self.read_only: return
        for i, line in enumerate(s.split('\n')):
            if i != 0:
                self.insert_newline()
            self.insert_no_newlines(line)

    def insert_newline(self):
        """Insert a newline at the cursor (as if it were typed)."""
        if self.read_only: return
        self.contents = (self.contents[:self.line]
                         + [self.contents[self.line][:self.point],
                            self.contents[self.line][self.point:]]
                         + self.contents[self.line + 1:])
        self.line += 1
        self.point = 0

    def cursor_up(self):
        if self.line > 0:
            self.line -= 1

    def cursor_left(self):
        if self.point > 0:
            self.point -= 1
        elif self.line > 0:
            self.line -= 1
            self.point = len(self.contents[self.line])

    def cursor_right(self):
        if self.point <= len(self.contents[self.line]):
            self.point += 1
        elif self.line < len(self.contents) - 1:
            self.point = 0
            self.line += 1

    def cursor_down(self):
        if self.line < len(self.contents) - 1:
            self.line += 1

    def delete_char_backwards(self):
        if self.read_only: return
        if self.point > 0:
            self.contents[self.line] = (self.contents[self.line][:self.point - 1]
                                        + self.contents[self.line][self.point:])
            self.point -= 1
        elif self.line > 0:
            self.point = len(self.contents[self.line - 1])
            self.contents = (self.contents[:self.line - 1]
                             + [self.contents[self.line - 1]
                                + self.contents[self.line]]
                             + self.contents[self.line + 1:])
            self.line -= 1

    def delete_char_forwards(self):
        if self.read_only: return
        if self.point < len(self.contents[self.line]):
            self.contents[self.line] = (self.contents[self.line][:self.point]
                                        + self.contents[self.line][self.point + 1:])
        elif self.line < len(self.contents) - 1:
            self.contents = (self.contents[:self.line]
                             + [self.contents[self.line]
                                + self.contents[self.line + 1]]
                             + self.contents[self.line + 2:])

    def delete_til_end_of_line(self):
        if self.read_only: return
        if self.point < len(self.contents[self.line]):
            self.clipboard = self.contents[self.line][self.point:]
            self.contents[self.line] = self.contents[self.line][:self.point]
        elif self.line < len(self.contents) - 1:
            self.clipboard = '\n'
            self.contents = (self.contents[:self.line]
                             + [self.contents[self.line]
                                + self.contents[self.line + 1]]
                             + self.contents[self.line + 2:])

    def yank(self):
        print self.clipboard
        self.insert(self.clipboard)

    def cursor_start_of_line(self):
        self.point = 0

    def cursor_end_of_line(self):
        self.point = len(self.contents[self.line])

    def scroll_to_point(self):
        self.scroll = self.line

    def scroll_up(self):
        if self.scroll > 0:
            self.scroll -= 1
        
    def scroll_down(self):
        if self.scroll < len(self.contents) - 1:
            self.scroll += 1

    # Event Handling
    def handle(self, event):
        """Handle pygame events."""
        if event.type == KEYDOWN:
            self.handle_keydown(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4: # Scroll wheel up
                self.scroll_up()
            elif event.button == 5: # Scroll wheel down
                self.scroll_down()
            
    def handle_keydown(self, event):
        """Handles keydown events given to the TextBox."""
        key = event.key
        if event.mod:
            mod = 0
            if event.mod & KMOD_CTRL:
                mod = mod | KMOD_CTRL
            if event.mod & KMOD_ALT:
                mod = mod | KMOD_CTRL
            if mod != 0:
                key = (mod, key)
            
        fn = self.bindings.get(key, None)
        if fn:
            fn()
        else:
            self.insert_no_newlines(event.unicode)
