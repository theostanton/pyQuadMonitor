import pygame
from pygame import gfxdraw

from Element import Element
from colors import *
import Data


gfx = pygame.gfxdraw
draw = pygame.draw

pygame.init()
font = pygame.font.Font(None, 20)


class Timings(Element):
    def __init__(self, surface):
        super(Timings, self).__init__(surface, "Timings")

    def draw(self):

        super(Timings, self).draw()

        tot = 0
        for val in Data.timings[1:]:
            tot += val
        pixperms = float(self.w) / (tot + 1)
        x = self.x

        for val, ratio, label in zip(Data.timings[1:], Data.ratios[1:], Data.timingsLabels[1:]):
            w = val * pixperms
            if val > 1000:
                rect = pygame.Rect(x, self.y, w, self.h)
                gfxdraw.rectangle(self.surface, rect, white)
                ren = font.render(label + " " + str(val) + " " + str(ratio), True, white)
                ren = pygame.transform.rotate(ren, -90.)
                self.surface.blit(ren, (rect.left, self.y + 20))
                x += w