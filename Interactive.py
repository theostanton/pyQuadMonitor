import pygame
from pygame import gfxdraw

from colors import *


gfx = pygame.gfxdraw
draw = pygame.gfxdraw

pygame.init()
font = pygame.font.Font(None, 20)

# States

IDLE = 0
DROP = 1

# Over

IDLE = 0
OVER = 1


class Interactive(object):
    def __init__(self, x, y, w, h, surface, label=None):
        self.surface = surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # No padding needed
        self.rect = pygame.Rect(x, y, w, h)

        self.dx = 0
        self.dy = 0

        self.fill = {}
        self.fill[IDLE] = gray_10
        self.fill[OVER] = white_40

        self.border = {}
        self.border[IDLE] = white_40
        self.border[OVER] = white

        self.label = label

        self.state = DROP
        self.over = IDLE

    def draw(self):
        pass

    def press(self, pos):
        pass

    def is_over(self, pos):
        pass

    def get_choice(self, pos):
        pass

    def offset(self, dx, dy):
        self.x -= self.dx
        self.y -= self.dy

        self.dx = dx
        self.dy = dy

        self.x += self.dx
        self.y += self.dy

        # No padding needed
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.drop_rect = pygame.Rect(self.x, self.y, self.w, self.h * len(self.choices))
