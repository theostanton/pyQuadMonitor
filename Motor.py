import pygame
from pygame import gfxdraw

from colors import *
from Element import Element
import Data


gfx = pygame.gfxdraw
draw = pygame.gfxdraw

pygame.init()
font = pygame.font.Font(None, 20)



class Motor(Element):
    def __init__(self, surface, motorid, label):
        super(Motor, self).__init__(surface, label)

        self.motorid = motorid
        self.pid = [10, 20, -10, -20]
        self.tot = 20
        self.gap = 0
        self.ww = 0


    def resize(self, x=None, y=None, w=None, h=None):
        super(Motor, self).resize(x, y, w, h)

        self.cy = y + h / 2
        self.gap = self.w / 13.
        self.ww = 2. * self.gap
        self.scale = self.h / 100.

    def draw(self):

        if not self.set:
            return

        x = self.x + self.gap

        gfx.rectangle(self.surface, self.rect, white)

        for t, v in zip('PIDT', Data.pid[self.motorid]):
            ren = font.render(t, True, white)
            self.surface.blit(ren, (x + self.ww / 2 - ren.get_width() / 2, self.cy - self.h / 4))

            rect = pygame.Rect(x, self.cy, self.ww, self.scale * v)
            gfx.box(self.surface, rect, white)
            x += self.ww + self.gap