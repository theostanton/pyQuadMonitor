from colors import *
import pygame
gfx = pygame.gfxdraw
pygame.init()
font = pygame.font.Font(None, 20, bold=False)

class Motor():

    def __init__(self,x,y,d,motorid):

        pad = 10
        self.motorid = motorid

        self.x = x + pad
        self.y = y + pad
        self.d = d - 2*pad
        self.cy = y + self.d / 2
        self.gap = self.d / 13
        self.w = 2 * self.gap

        self.rect = pygame.Rect( self.x,self.y,self.d,self.d )
        self.pid = [10, 20, -10, -20]
        self.tot = 20

    def put(self,pid):
        #print self.motorid,
        #print pid
        self.tot = 0
        self.pid = []
        for v in pid:
            self.pid.append( v/1000 )
            self.tot += v/1000
        self.pid.append( self.tot )

    def draw(self,surface):

        x = self.x + self.gap

        gfx.rectangle(surface, self.rect, white)


        for t,v in zip('PIDT',self.pid):

            ren = font.render(t,True,white)
            surface.blit(ren,(x+self.w/2-ren.get_width()/2,self.cy - self.d/4))

            rect = pygame.Rect( x, self.cy, self.w, 4 * v)
            gfx.box( surface, rect,white )
            x += self.w + self.gap