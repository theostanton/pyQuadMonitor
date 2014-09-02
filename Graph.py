import numpy
import pygame
from pygame import gfxdraw
from colors import *
gfx = pygame.gfxdraw
draw = pygame.gfxdraw
from collections import defaultdict

pygame.init()
font = pygame.font.Font(None, 20, bold=False)

class Graph():

    def __init__(self, x,y,w,h, axisid, angleids, label):
        self.axisid = axisid
        self.angleids = angleids
        self.label = label
        pad = 10

        self.x = x + pad
        self.y = y + pad
        self.cy = y + h/2
        self.w = w - 2*pad
        self.h = h - 2*pad
        self.rect = pygame.Rect( self.x, self.y, self.w, self.h )

    def draw(self, surface, logs):

        for angleid in self.angleids:

            x = self.x
            y = self.cy

            points = []
            points.append( (x,y) )
            for val in reversed( logs[angleid] ):

                points.append( ( x, y + val[self.axisid] ) )
                x += 1

                if x >= self.x + self.w:
                    break

            points.append( (x-1,y) )

            if len(points) > 2:
                draw.aapolygon( surface, points, colors[angleid] )

        gfx.hline( surface, self.x, self.x+self.w-1, self.cy, white )
        gfx.rectangle( surface, self.rect, white )