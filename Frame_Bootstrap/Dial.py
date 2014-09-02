import numpy as np
import pygame
from Element import Element
from pygame import gfxdraw
from colors import *
import Dropdown
gfx = pygame.gfxdraw
draw = pygame.draw

pygame.init()
font = pygame.font.Font(None, 20)

# Axis ids
ROLL = 0
PITCH = 1
YAW = 2

class Dial(Element):

    def __init__(self,surface,axisid, angleids,label):
        super(Dial,self).__init__(surface,label)
        self.axisid = axisid
        self.angleids = angleids

        self.angles = {}
        for a in 'AGMDE':
            self.angles[a] = [0,0,0]

    def draw(self):
        if not self.set:
            return


        cx = self.rect.centerx
        cy = self.rect.centery

        gfx.filled_circle(self.surface, cx,cy, self.r, gray_10)

        gfx.line(self.surface,self.x,cy,self.rect.right,cy,white)

        #label after fill
        super(Dial,self).draw()

        for a in range(0,179,45):
            dx = int( self.r * np.sin( np.radians(  a + 90) ) )
            dy = int( self.r * np.cos( np.radians(  a + 90) ) )
            gfx.line( self.surface, cx - dx, cy - dy, cx + dx, cy + dy, white_40 )

        for angleid  in self.angleids:

            dx = int( self.r * np.sin( np.radians( self.angles[angleid][self.axisid] + 90 ) ) )
            dy = int( self.r * np.cos( np.radians( self.angles[angleid][self.axisid] + 90 ) ) )

            lx = cx - dx
            ly = cy - dy
            rx = cx + dx
            ry = cy + dy

            gfx.line( self.surface, lx,ly,rx,ry, colors[angleid] )

            if angleid is 'M':
                scale = 5
                bars = [0,0,0,0]

                if self.axisid is PITCH:
                    bars[0] = 50
                    bars[1] = 40
                    bars[2] = 30
                    bars[3] = 20

                else :
                    bars[0] = 10
                    bars[1] = 20
                    bars[2] = 30
                    bars[3] = 40

                draw.line(self.surface, (255,0,0), (lx - 2, ly) , ( lx - 2, ly+bars[0]), 5, )
                draw.line(self.surface, (255,0,0), (lx + 2, ly) , ( lx + 2, ly+bars[1]), 5, )
                draw.line(self.surface, (255,0,0), (rx - 2, ry) , ( rx - 2, ry+bars[2]), 5, )
                draw.line(self.surface, (255,0,0), (rx + 2, ry) , ( rx + 2, ry+bars[3]), 5, )

        gfx.aacircle(self.surface, cx,cy, self.r, white)