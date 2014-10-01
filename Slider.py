from pygame import gfxdraw

from Element import *
from colors import *


gfx = pygame.gfxdraw
draw = pygame.draw

pygame.init()
font = pygame.font.Font(None, 20)


class Slider(Element):
    def __init__(self, surface, min=0, max=1000, label="Slider"):
        super(Slider, self).__init__(surface, label)

        self.min = min
        self.max = max
        self.val = ( max - min ) / 2 + min

        self.val_rect = None

        self.butt_w = 10


    def resize(self, x=None, y=None, w=None, h=None):
        super(Slider, self).resize(x, y, w, h)

        self.perc = (self.val - self.min ) / (self.max - self.min)
        x = self.x + self.w * self.perc
        self.val_rect = pygame.Rect(x + 1 - self.butt_w / 2, self.y + 1, self.butt_w, self.h - 2)


    def draw(self):

        # label
        ren = font.render(self.label, True, white)
        self.surface.blit(ren, (self.x + 10, self.y + self.h / 2 - ren.get_height() / 2 ))

        # value
        ren = font.render(str(int(self.val)), True, white)
        self.surface.blit(ren, (self.rect.right - 10 - ren.get_width(), self.y + self.h / 2 - ren.get_height() / 2 ))
        # "{:10.4f}".format(x)

        gfx.rectangle(self.surface, self.rect, self.fill[self.state])
        gfx.box(self.surface, self.val_rect, self.fill[self.state])

    def sett(self, val):
        self.val = val

    def set_x(self, x):

        if x < self.x:
            x = self.x
        elif x > self.rect.right:
            x = self.rect.right

        self.perc = float(x - self.x) / float(self.w)
        print x, self.x, self.w, self.perc
        self.val = ( self.max - self.min ) * self.perc + self.min

        self.val_rect = pygame.Rect(x + 1 - self.butt_w / 2, self.y + 1, self.butt_w, self.h - 2)

    def is_over(self, pos):
        super(Slider, self).is_over(pos)

        if self.rect.collidepoint(pos):
            if self.state is DRAG:
                self.set_x(pos[0])
            self.state = OVER
        else:
            self.state = IDLE

    def move_over(self, pos, rel):

        if self.state is DRAG:
            self.val_rect.x += rel[0]
            self.set_x(pos[0])
            return True

        if self.rect.collidepoint(pos):
            self.state = OVER
            return True
        else:
            self.state = IDLE

        return False

    def press(self, pos):

        if self.state is DRAG:
            self.state = OVER
            return

        if self.rect.collidepoint(pos):
            self.state = DRAG
            self.set_x(pos[0])
            return True
        else:
            self.state = IDLE
            return False



