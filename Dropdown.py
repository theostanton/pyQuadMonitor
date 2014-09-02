import pygame
from colors import *
from pygame import gfxdraw
gfx = pygame.gfxdraw
draw = pygame.gfxdraw

pygame.init()
font = pygame.font.Font(None, 20)

# States

IDLE = 0
DROP = 1

# Over

IDLE = 0
OVER = 1


class DropDown(object):

    def __init__(self,x,y,w,h,surface,label=None,choices=None):
        self.surface = surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # No padding needed
        self.rect = pygame.Rect(x,y,w,h)

        self.dx = 0
        self.dy = 0

        self.fill = {}
        self.fill[IDLE] = gray_10
        self.fill[OVER] = white_40

        self.border = {}
        self.border[IDLE] = white_40
        self.border[OVER] = white

        self.label = label
        self.choices = choices

        self.drop_rect = pygame.Rect(x,y,w,h*len(choices))

        self.state = DROP
        self.over = IDLE

    def draw(self):

        if self.state is IDLE:
            gfx.box( self.surface, self.rect, self.fill[self.over>0] )
            gfx.rectangle( self.surface, self.rect, self.border[self.over>0] )
            if self.label is not None:
                ren = font.render(self.label,True,self.border[self.over>0])
                self.surface.blit(ren,(self.rect.centerx-ren.get_width()/2,self.rect.top + ren.get_height()/2))

        elif self.state is DROP:
            #n = len(self.choices)
            #rect = pygame.Rect(self.x,self.y,self.w,n*self.h)
            if self.over:
                gfx.box( self.surface, self.drop_rect, self.fill[IDLE] )
                gfx.rectangle( self.surface, self.drop_rect, self.border[IDLE] )
                y = self.y + self.over * self.h
                rect = pygame.Rect(self.x,y,self.w,self.h)
                gfx.box( self.surface, rect, self.fill[OVER] )
                gfx.rectangle( self.surface, rect, self.border[OVER] )
            else :
                gfx.box( self.surface, self.drop_rect, self.fill[IDLE] )
                gfx.rectangle( self.surface, self.drop_rect, self.border[IDLE] )

            y = self.y
            for choice in self.choices:
                ren = font.render(choice,True,self.border[self.over > 0])
                self.surface.blit(ren,(self.rect.centerx-ren.get_width()/2,y + ren.get_height()/2))
                y += self.h

    def offset(self,dx,dy):

        self.x -= self.dx
        self.y -= self.dy

        self.dx = dx
        self.dy = dy

        self.x += self.dx
        self.y += self.dy

        # No padding needed
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.drop_rect = pygame.Rect(self.x,self.y,self.w,self.h*len(self.choices))

    def press(self,pos):

        if self.state is IDLE:
            if self.rect.collidepoint(pos):
                self.state = DROP
        else:
            if self.drop_rect.collidepoint(pos):
                self.state = IDLE

    def is_over(self,pos):

        if self.state is IDLE:
            if self.rect.collidepoint(pos):
                self.over = OVER
                return

        elif self.state is DROP:
            if self.drop_rect.collidepoint(pos):
                self.over = ( pos[1] - self.y ) / self.h
                print self.over
                #self.over = OVER
                return

        self.over = IDLE



