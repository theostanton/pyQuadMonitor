import pygame
from pygame import gfxdraw

import Data
from colors import *


gfx = pygame.gfxdraw
draw = pygame.draw

pygame.init()
font = pygame.font.Font(None, 20)

# States
IDLE = 0
OVER = 1
DRAG = 2

# Transition states
IDLE = 0
GOOVER = 1
GOIDLE = 2
GODRAG = 3


class Element(object):

    def __init__(self, surface, label=None):

        self.set = False

        self.surface = surface

        self.state = IDLE

        self.fill = {}
        self.fill[IDLE] = white_40
        self.fill[OVER] = white
        self.fill[DRAG] = white

        self.border = {}
        self.border[IDLE] = white
        self.border[DRAG] = red

        self.label = label

        self.pad = 10

        self.interactives = []
        # self.interactives.append(Dropdown.DropDown(10, 10, 60, 25, surface, 'Label', ('One', 'Two', 'Three', 'Four')))

        self.transition_diff = []  # (float, float, float) to be acced to current colour


    def resize(self, x=None, y=None, w=None, h=None):

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

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        for interactive in self.interactives:
            interactive.offset(self.x, self.y)

        self.set = True

    def draw(self):

        if not self.set:
            return

        if self.state is OVER:
            print self.label,'over'
            for interactive in self.interactives:
                interactive.draw()

        # gfx.box( self.surface, self.rect, self.fill[self.state] )
        # gfx.rectangle( self.surface, self.rect, self.border[self.state] )

        if self.label is not None:
            ren = font.render(self.label, True, white)
            self.surface.blit(ren, (self.rect.centerx - ren.get_width() / 2, self.rect.top + ren.get_height()))

    def is_over(self, pos):
        for interactive in self.interactives:
            interactive.is_over(pos)

    def add_interactive(self, interactive):
        interactive.offset(self.x, self.y)
        self.interactives.append(interactive)

    def press(self, pos):

        for interactive in self.interactives:
            if interactive.press(pos):
                print interactive.get_choice(pos)

    def move_over(self, pos, rel):
        if self.rect.collidepoint(pos):
            self.state = OVER
        elif self.state is OVER:
            self.state = IDLE

    def tick_transition(self):
        pass

    def start_transition(self):
        pass
