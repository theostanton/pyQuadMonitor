import pygame
import numpy as np
from colors import *
from pygame import gfxdraw
gfx = pygame.gfxdraw
draw = pygame.draw


ROLL = 0
PITCH = 1
YAW = 2

pygame.init()
font = pygame.font.Font(None, 20, bold=False)

class Dial():

    def __init__(self,x,y,r,axisid,angleids, label):
        self.axisid = axisid
        self.angleids = angleids
        self.label = label
        pad = 10
        #self.rect = pygame.Rect(x,y,w,h)
        self.x = x + pad
        self.cx = x + r
        self.y = y + pad
        self.cy = y + r
        self.r = r - 2 * pad

    def draw(self,surface, angles, motors):

        gfx.line(surface, self.cx - self.r,self.cy,self.cx + self.r, self.cy,white)

        ren = font.render(self.label,True,white)

        surface.blit(ren,(self.cx-ren.get_width() / 2,self.cy - self.r / 2))

        for a in range(0,179,45):
            dx = int( self.r * np.sin( np.radians(  a + 90) ) )
            dy = int( self.r * np.cos( np.radians(  a + 90) ) )
            gfx.line( surface, self.cx - dx, self.cy - dy, self.cx + dx, self.cy + dy, white_40 )
            #draw.line( surface, (255,255,255,1), (self.cx - dx, self.cy - dy), (self.cx + dx, self.cy + dy) )

        for angleid  in self.angleids:

            dx = int( self.r * np.sin( np.radians( angles[angleid][self.axisid] + 90 ) ) )
            dy = int( self.r * np.cos( np.radians( angles[angleid][self.axisid] + 90 ) ) )

            lx = self.cx - dx
            ly = self.cy - dy
            rx = self.cx + dx
            ry = self.cy + dy

            #draw.aaline( surface, colors[angleid], (lx,ly),(rx,ry) )
            gfx.line( surface, lx,ly,rx,ry, colors[angleid] )

            if angleid is 'M':
                scale = 5
                bars = [0,0,0,0]

                if self.axisid is PITCH:
                    bars[0] = scale * motors['a'].tot
                    bars[1] = scale * motors['b'].tot
                    bars[2] = scale * motors['c'].tot
                    bars[3] = scale * motors['d'].tot

                else :
                    bars[0] = scale * motors['b'].tot
                    bars[1] = scale * motors['d'].tot
                    bars[2] = scale * motors['a'].tot
                    bars[3] = scale * motors['c'].tot

                draw.line(surface, (255,0,0), (lx - 2, ly) , ( lx - 2, ly+bars[0]), 5)
                draw.line(surface, (255,0,0), (lx + 2, ly) , ( lx + 2, ly+bars[1]), 5)
                draw.line(surface, (255,0,0), (rx - 2, ry) , ( rx - 2, ry+bars[2]), 5)
                draw.line(surface, (255,0,0), (rx + 2, ry) , ( rx + 2, ry+bars[3]), 5)

        gfx.aacircle(surface, self.cx, self.cy, self.r, white)