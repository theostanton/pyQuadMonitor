import pygame
from colors import *
from pygame import gfxdraw
import Dropdown
gfx = pygame.gfxdraw
draw = pygame.draw

pygame.init()
font = pygame.font.Font(None, 20)

# States
IDLE = 0
OVER = 1








class Element(object):

    def __init__(self,surface,label=None):

        self.set = False

        self.surface = surface

        self.state = IDLE

        self.fill = {}
        self.fill[IDLE] = white_40
        #self.fill[OVER] = white

        self.border = {}
        self.border[IDLE] = white
        #self.border[OVER] = red

        self.label = label

        self.pad = 10

        self.interactives = []
        self.interactives.append( Dropdown.DropDown(10,10,60,25,surface,'Label',('One','Two','Three','Four')) )

    def resize(self,x=None,y=None,w=None,h=None):

        '''
        :param x: do
        :param y: asd
        :param w: ass
        :param h: asd
        :return: asd
        '''

        if x is not None:
            self.x = x + self.pad
        if y is not None:
            self.y = y + self.pad
        if w is not None:
            self.w = w - 2 * self.pad
            self.r = self.w / 2
        if h is not None:
            self.h = h - 2 * self.pad

        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

        for interactive in self.interactives:
            interactive.offset(self.x,self.y)

        self.set = True

    def draw(self):

        if not self.set:
            return

        for interactive in self.interactives:
            interactive.draw()

        # gfx.box( self.surface, self.rect, self.fill[self.state] )
        # gfx.rectangle( self.surface, self.rect, self.border[self.state] )

        if self.label is not None:
            ren = font.render(self.label,True,white)
            self.surface.blit(ren,(self.rect.centerx-ren.get_width()/2,self.rect.top + ren.get_height()))

    def is_over(self,pos):
        for interactive in self.interactives:
            interactive.is_over(pos)

    def add_interactive(self,interactive):
        interactive.offset(self.x,self.y)
        self.interactives.append(interactive)

    def press(self,pos):

        for interactive in self.interactives:
            interactive.press(pos)


