import pygame
from pygame.locals import *

def blit_text(surface, text, x, y, font=None, color=(255, 255, 255)):
    """Display a string on a surface centred at x & y."""
    if not font:
        font = pygame.font.Font(None, 14)
    text = font.render(text, True, color) # True for antialiasing
    pos = text.get_rect(x = x, y = y)
    surface.blit(text, pos)

