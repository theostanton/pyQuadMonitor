import pygame
from pygame import gfxdraw

from Interactive import Interactive


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


class DropDown(Interactive):
    def __init__(self, x, y, w, h, surface, label=None, choices=None):

        super(DropDown, self).__init__(x, y, w, h, surface, label)

        self.state = IDLE
        self.choices = choices

        self.drop_rect = pygame.Rect(x, y, w, h * len(choices))


    def draw(self):
        if self.state is IDLE:
            # gfx.box(self.surface, self.rect, self.fill[self.over > 0])
            gfx.rectangle(self.surface, self.rect, self.border[self.over > 0])
            if self.label is not None:
                ren = font.render(self.label, True, self.border[self.over > 0])
                self.surface.blit(ren, (self.rect.centerx - ren.get_width() / 2, self.rect.top + ren.get_height() / 2))

        elif self.state is DROP:
            # n = len(self.choices)
            #rect = pygame.Rect(self.x,self.y,self.w,n*self.h)
            if self.over:
                gfx.box(self.surface, self.drop_rect, self.fill[IDLE])
                gfx.rectangle(self.surface, self.drop_rect, self.border[IDLE])
                y = self.y + self.over * self.h
                rect = pygame.Rect(self.x, y, self.w, self.h)
                gfx.box(self.surface, rect, self.fill[OVER])
                gfx.rectangle(self.surface, rect, self.border[OVER])
            else:
                gfx.box(self.surface, self.drop_rect, self.fill[IDLE])
                gfx.rectangle(self.surface, self.drop_rect, self.border[IDLE])

            y = self.y
            for choice in self.choices:
                ren = font.render(choice, True, self.border[self.over > 0])
                self.surface.blit(ren, (self.rect.centerx - ren.get_width() / 2, y + ren.get_height() / 2))
                y += self.h

    def press(self, pos):

        if self.state is IDLE:
            if self.rect.collidepoint(pos):
                self.state = DROP
            return False

        else:
            self.state = IDLE
            return self.drop_rect.collidepoint(pos)

    def is_over(self, pos):

        if self.state is IDLE:
            if self.rect.collidepoint(pos):
                self.over = OVER
                return

        elif self.state is DROP:
            if self.drop_rect.collidepoint(pos):
                self.over = ( pos[1] - self.y ) / self.h
                print self.over

                # self.over = OVER
                return

        self.over = IDLE

    def get_choice(self, pos):

        for y, choice in zip(range(self.y, self.drop_rect.bottom, self.h), self.choices):
            if pos[1] > y and pos[1] < y + self.h:
                return choice

        return 'k'

        for choice, rect_choice in zip(self.choices, self.choice_rects):
            print rect_choice
            print pos
            if rect_choice.collidepoint(pos):
                print 'collides with', choice
                return choice
        print 'Error'

    def offset(self, dx, dy):
        super(DropDown, self).offset(dx, dy)

        y = self.y
        self.choice_rects = []
        for choice in self.choices:
            self.choice_rects.append(pygame.Rect(self.x, y, self.w, self.h))
            y += self.h
