import numpy as np
import pygame
from pygame import gfxdraw

from Element import Element
from colors import *
import Data


gfx = pygame.gfxdraw
draw = pygame.draw

pygame.init()
font = pygame.font.Font(None, 20)

# Axis ids
ROLL = 0
PITCH = 1
YAW = 2


class Dial(Element):
    def __init__(self, surface, axisid, angleids, label):
        super(Dial, self).__init__(surface, label)
        self.axisid = axisid
        self.angleids = angleids

        # self.angles = {}
        # for a in 'AGMDE':
        # self.angles[a] = [0,0,0]

    def draw(self):
        if not self.set:
            return

        cx = self.rect.centerx
        cy = self.rect.centery

        gfx.filled_circle(self.surface, cx, cy, self.r, gray_10)

        gfx.line(self.surface, self.x, cy, self.rect.right, cy, white)

        # label after fill
        super(Dial, self).draw()

        for a in range(0, 179, 45):
            dx = int(self.r * np.sin(np.radians(a + 90)))
            dy = int(self.r * np.cos(np.radians(a + 90)))
            gfx.line(self.surface, cx - dx, cy - dy, cx + dx, cy + dy, white_40)

        for angleid in self.angleids:

            dx = int(self.r * np.sin(np.radians(Data.angles[angleid][self.axisid] + 90)))
            dy = int(self.r * np.cos(np.radians(Data.angles[angleid][self.axisid] + 90)))

            lx = cx - dx
            ly = cy - dy
            rx = cx + dx
            ry = cy + dy

            gfx.line(self.surface, lx, ly, rx, ry, colors[angleid])

            if angleid is 'M':
                scale = 5
                bars = {}
                #
                # if self.axisid is PITCH:
                bars['a'] = Data.pid['a'][3] * 20
                bars['b'] = Data.pid['b'][3] * 20
                bars['c'] = Data.pid['c'][3] * 20
                bars['d'] = Data.pid['d'][3] * 20

                # else:
                #     bars[0] = Data.pid['a'][3] * 20
                #     bars[1] = Data.pid['c'][3] * 20
                #     bars[2] = Data.pid['b'][3] * 20
                #     bars[3] = Data.pid['d'][3] * 20

                draw.line(self.surface, colors['a'], (lx - 2, ly), ( lx - 2, ly + bars['a']), 2, )
                draw.line(self.surface, colors['b'], (lx + 2, ly), ( lx + 2, ly + bars['b']), 2, )
                draw.line(self.surface, colors['c'], (rx - 2, ry), ( rx - 2, ry + bars['c']), 2, )
                draw.line(self.surface, colors['d'], (rx + 2, ry), ( rx + 2, ry + bars['d']), 2, )

        gfx.aacircle(self.surface, cx, cy, self.r, white)