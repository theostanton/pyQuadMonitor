import numpy as np
from pygame import gfxdraw

from Element import *
from colors import *


gfx = pygame.gfxdraw
draw = pygame.gfxdraw

pygame.init()
font = pygame.font.Font(None, 20, bold=False)

# States
IDLE = 0
DRAG = 1
OVER = 2
SIZE = 3  # TODO this is silly

# Layouts
GRID = 0
VERT = 1

# Aspect Ratios
NO_AR = 0
FIXED_AR = 1

# Controls
ctrl_rect_d = 10
KILL = 1
FULL = 2
SIZE = 3  # TODO this is silly
LOCK = 4


class Frame():
    def __init__(self, x, y, w, h, surface, pad=10, label="NA", layout=GRID, AR=NO_AR, empty_BG=False):
        self.AR = AR
        self.surface = surface
        self.pad = pad
        self.x = x + pad
        self.y = y + pad
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w - 2 * self.pad, self.h - 2 * self.pad)
        self.ctrl_rect = pygame.Rect(self.rect.right - ctrl_rect_d, self.rect.bottom - ctrl_rect_d, ctrl_rect_d,
                                     ctrl_rect_d)

        self.empty_BG = empty_BG

        self.border = {}
        self.border[IDLE] = white
        self.border[DRAG] = white
        self.border[OVER] = white
        self.border[SIZE] = red

        self.fill = {}
        self.fill[IDLE] = white_40
        self.fill[DRAG] = white
        self.fill[OVER] = white
        self.fill[SIZE] = white

        self.lock = False
        self.state = IDLE

        self.label = label

        self.dragging = False
        self.moved = False
        self.over = False

        self.elements = []
        self.n_elements = 0
        self.layout = layout

        self.full = False

        self.controls = Controls(surface)
        self.controls.add_button(Button(surface, SIZE))
        self.controls.add_button(Button(surface, FULL))
        self.controls.add_button(Button(surface, KILL))
        self.controls.add_button(Button(surface, LOCK))
        self.controls.resize(self.rect.right, self.rect.bottom)

    def add_element(self, element=None):
        if element == None:
            element = Element.Element(self.surface)

        self.elements.append(element)
        self.n_elements = len(self.elements)

        self.resize_elements()

    def set_full(self, full):
        if self.full is not full:
            self.toggle_full()


    def toggle_full(self):
        if self.full:
            self.pad = self.old_pad
            self.x = self.old_x
            self.y = self.old_y
            self.w = self.old_w
            self.h = self.old_h
            self.full = False
        else:
            self.old_x, self.old_y, self.old_w, self.old_h = self.x, self.y, self.w, self.h
            self.old_pad = self.pad
            self.pad = 0
            self.x = 0
            self.y = 0
            self.w = self.surface.get_width()
            self.h = self.surface.get_height()
            self.full = True
            self.lock = True
        self.set()

        if self.AR is FIXED_AR:
            if self.w < self.surface.get_width():
                self.x = self.surface.get_width() - self.w
                self.x /= 2
            elif self.h < self.surface.get_height():
                self.y = self.surface.get_height() - self.h
                self.y /= 2
        self.set()


    def resize_elements(self):

        margin = self.pad
        margin_rect = pygame.Rect(self.x + margin, self.y + margin, self.w - 2 * margin, self.h - 2 * margin)

        if self.n_elements is 0:
            return

        if self.layout is GRID:

            # TODO : actual maths
            if self.n_elements is 4:
                per_row = 2
            else:
                per_row = int(np.sqrt(self.n_elements))
            # per_row = 2
            per_col = int(np.sqrt(self.n_elements))
            print 'per', per_row

            i = 0
            w = margin_rect.width / per_row
            h = margin_rect.height / per_col
            x = self.x
            y = self.y

            for col in range(per_col):
                for row in range(per_row):
                    self.elements[i].resize(x, y, w, h)
                    i += 1
                    x += w
                y += h
                x = self.x

        elif self.layout is VERT:

            dy = margin_rect.height / self.n_elements
            y = self.y

            for element in self.elements:
                element.resize(self.x, y, margin_rect.width, dy)
                y += dy


    def set(self):

        if self.AR is FIXED_AR:
            if self.w != self.h:
                self.w = self.h = min(self.w, self.h)
        self.rect = pygame.Rect(self.x, self.y, self.w - 2 * self.pad, self.h - 2 * self.pad)
        self.ctrl_rect = pygame.Rect(self.rect.right - ctrl_rect_d, self.rect.bottom - ctrl_rect_d, ctrl_rect_d,
                                     ctrl_rect_d)
        self.resize_elements()
        self.controls.resize(self.rect.right, self.rect.bottom)

        # print 'rect', self.rect

    def draw_if_full(self):
        if self.full:
            self.draw()

    def draw(self):

        if self.moved:
            self.set()
            self.moved = False

        if not self.empty_BG and not self.full and not self.lock:
            gfx.box(self.surface, self.rect, self.fill[self.state])
            gfx.rectangle(self.surface, self.rect, self.border[self.state])

        if self.state in (DRAG, OVER, SIZE):
            # gfx.box( self.surface, self.ctrl_rect, self.fill[self.state] )
            # gfx.rectangle( self.surface, self.ctrl_rect, self.border[self.state] )
            self.controls.draw()

        for element in self.elements:
            element.draw()

    def press(self, pos):

        for element in self.elements:
            if element.press(pos):
                return

        ctrl_press = self.controls.press(pos)
        if ctrl_press:
            if ctrl_press is SIZE and not self.full:
                self.state = SIZE
            elif ctrl_press is KILL:
                print 'kill', self.label
                return ctrl_press
            elif ctrl_press is FULL:
                print 'full', self.label
                self.toggle_full()
                return ctrl_press
            elif ctrl_press is LOCK:
                self.lock = not self.lock

        elif not self.lock and self.rect.collidepoint(pos):
            if self.state is not DRAG:
                print 'dragging', self.label
            self.state = DRAG

        else:
            self.state = IDLE

        return 0

    def release(self, pos):
        self.state = IDLE

    def move_over(self, pos, rel):

        for element in self.elements:
            if element.move_over(pos, rel):
                return

        if self.state is SIZE:
            dx, dy = rel

            if self.AR == FIXED_AR:
                if abs(dx) > abs(dy):
                    dy = dx
                else:
                    dx = dy

            self.w += dx
            self.h += dy

            if self.x + self.w > self.surface.get_width() + 2 * self.pad:
                self.w = self.surface.get_width() - self.x + 2 * self.pad

            if self.y + self.h > self.surface.get_height() + 2 * self.pad:
                self.h = self.surface.get_height() - self.y + 2 * self.pad

            self.moved = True
            self.set()
            return True

        elif self.state is DRAG:
            print self.x, self.y,
            dx, dy = rel
            self.x += dx
            self.y += dy

            if self.x < 0:
                self.x = 0

            if self.y < 0:
                self.y = 0

            if self.x + self.w > self.surface.get_width() + 2 * self.pad:
                self.x = self.surface.get_width() - self.w + 2 * self.pad

            if self.y + self.h > self.surface.get_height() + 2 * self.pad:
                self.y = self.surface.get_height() - self.h + 2 * self.pad

            # print rel, self.x, self.y
            self.moved = True
            return True

        elif self.rect.collidepoint(pos):
            self.state = OVER
        else:
            self.state = IDLE
        return False


class Controls:
    def __init__(self, surface):

        self.surface = surface
        self.buttons = []

        self.set = False

    def add_button(self, button):

        self.buttons.append(button)
        self.resize_buttons()

    def resize(self, right, bottom):
        self.right = right
        self.bottom = bottom
        self.set = True
        self.resize_buttons()

    def resize_buttons(self):

        if not self.set:
            return

        x = self.right - ctrl_rect_d
        y = self.bottom - ctrl_rect_d

        for b in self.buttons:
            b.resize(x, y)
            x -= ctrl_rect_d

    def draw(self):

        for b in self.buttons:
            b.draw()

    def press(self, pos):

        for b in self.buttons:
            if b.press(pos):
                return b.press(pos)
        return 0

    def move_over(self, pos):
        over = False
        for b in self.buttons:
            if b.move_over(pos):
                over = True
        return over


class Button(Element):
    def __init__(self, surface, id=SIZE):
        super(Button, self).__init__(surface)
        self.w = ctrl_rect_d
        self.h = ctrl_rect_d
        self.pad = 0
        self.id = id

        self.state = IDLE

        self.fill = {}
        self.fill[IDLE] = white_40
        self.fill[OVER] = white

        self.border = {}
        self.border[IDLE] = white
        self.border[OVER] = red

    def draw(self):
        gfx.box(self.surface, self.rect, self.fill[self.state])
        gfx.rectangle(self.surface, self.rect, self.border[self.state])

    def press(self, pos):
        if self.rect.collidepoint(pos):
            return self.id
        return 0

    def move_over(self, pos):

        if self.rect.collidepoint(pos):
            self.state = OVER
            return True
        else:
            self.state = IDLE
            return False