import pygame
from pygame import gfxdraw
from colors import *
gfx = pygame.gfxdraw
draw = pygame.gfxdraw

pygame.init()
font = pygame.font.Font(None, 20, bold=False)

class Slider():

    def __init__(self ,x ,y ,w ,h, id, max ):
        pad = 10
        self.x = x + pad
        self.y = y + pad
        self.w = w - 2*pad
        self.h = h - 2*pad
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h )

        self.id = id
        self.max = max
        self.val = self.max / 2

    def draw(self,surface):

        gfx.rectangle( surface, self.rect, white )
        box = pygame.Rect( self.x, self.y, self.val * self.w / self.max, self.h )
        gfx.box( surface, box, white )

    def isover(self, pos):
        if self.rect.collidepoint(pos):
            dx = pos[0] - self.x
            self.val = dx * self.max / self.w
            print self.val
            return self.id, self.val
        return 0