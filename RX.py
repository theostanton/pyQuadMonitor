import pygame
from pygame import gfxdraw

from Element import Element
from colors import *
import Data


gfx = pygame.gfxdraw
draw = pygame.draw

pygame.init()
font = pygame.font.Font(None, 20)


class RX(Element):
    def __init__(self, surface):
        super(RX, self).__init__(surface, "")

    def draw(self):
        super(RX, self).draw()

        x_scale = self.w / 20000.
        # print 'x_scale', x_scale
        dy = self.h / 6

        y = self.y
        x = self.x
        prev = 0

        for val in Data.rx:
            ww = val * x_scale
            # print val,
            # print 'val', val,
            # print 'ww', ww,
            rect = pygame.Rect(x, y, ww, dy)
            gfxdraw.box(self.surface, rect, (200, 200, 200))

            ren = font.render(str(val), True, white)
            self.surface.blit(ren, (self.rect.right - ren.get_width(), y + ren.get_height() / 2))

            y += dy
            prev = val
            x += ww
            # print ''


            # gfx.box(self.surface, self.rect,(255,200,100))
