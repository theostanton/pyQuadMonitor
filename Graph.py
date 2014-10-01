import pygame
from pygame import gfxdraw

import Dropdown
from Element import Element
from colors import *
import Data


gfx = pygame.gfxdraw
draw = pygame.draw

pygame.init()
font = pygame.font.Font(None, 20)


class Graph(Element):
    def __init__(self, surface, axisid, angleids, label):
        super(Graph, self).__init__(surface, label)
        self.axisid = axisid
        self.angleids = angleids

        self.interactives.append(Dropdown.DropDown(10, 10, 60, 25, surface, 'Axis', ('Roll', 'Pitch', 'Yaw')))

    def resize(self, x=None, y=None, w=None, h=None):
        super(Graph, self).resize(x, y, w, h)
        self.cy = y + h/2

    def press(self, pos):

        for interactive in self.interactives:
            if interactive.press(pos):
                self.set_axisid(interactive.get_choice(pos))
                print 'axisid set to', self.axisid

    def set_axisid(self, label):
        self.label = label
        if label in 'Roll':
            self.axisid = 0
        elif label in 'Pitch':
            self.axisid = 1
        else:
            self.axisid = 2

    def draw(self):

        if not self.set:
            return

        super(Graph, self).draw()

        x_scale = self.h / 2
        x_scale /= 45.

        for angleid in self.angleids:

            x = self.x
            y = self.cy

            points = []
            for val in reversed(Data.angle_log[angleid]):
                x += 2
                y = val[self.axisid] * x_scale
                points.append((x, self.cy + y))
                if x > self.x + self.w:
                    break
            points.append((self.x + self.w, self.cy))


            # # aalines(Surface, color, closed, pointlist, blend=1) -> Rect

            try:
                if len(points) > 2:
                    pygame.draw.aalines(self.surface, colors[angleid], False, points)
            except Exception as e:
                print 'error..', e.message

        gfx.hline(self.surface, self.x, self.x + self.w - 1, self.cy, white)
        gfx.rectangle(self.surface, self.rect, white)