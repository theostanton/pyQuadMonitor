import numpy
import pygame
from Element import Element
from pygame import gfxdraw
from colors import *
gfx = pygame.gfxdraw
draw = pygame.gfxdraw
from collections import defaultdict

pygame.init()
font = pygame.font.Font(None, 20)

class Graph(Element):

    def __init__(self, surface, axisid, angleids, label):
        super(Graph,self).__init__(surface,label)
        self.axisid = axisid
        self.angleids = angleids

    def resize(self,x=None,y=None,w=None,h=None):
        super(Graph,self).resize(x,y,w,h)
        self.cy = y + h/2


    def draw(self):

        if not self.set:
            return

        super(Graph,self).draw()

        for angleid in self.angleids:

            x = self.x
            y = self.cy

            points = []
            points.append( (x,y) )


            points.append( (x-1,y) )

            if len(points) > 2:
                draw.aapolygon( self.surface, points, colors[angleid] )

        gfx.hline( self.surface, self.x, self.x+self.w-1, self.cy, white )
        gfx.rectangle( self.surface, self.rect, white )