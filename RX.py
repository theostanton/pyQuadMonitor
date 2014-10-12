from Element import *

channels = ("Roll","Throttle","Pitch","Yaw","Aux 1", "Aux 2")

class RX(Element):
    def __init__(self, surface):
        super(RX, self).__init__(surface, "")

    def draw(self):
        super(RX, self).draw()

        x_scale = self.w / 12000.
        # print 'x_scale', x_scale
        dy = self.h / 6

        y = self.y
        x = self.x
        prev = 0

        for val,channel in zip(Data.rx,channels):
            ww = val * x_scale
            # print val,
            # print 'val', val,
            # print 'ww', ww,
            rect = pygame.Rect(x, y, ww, dy)
            gfxdraw.box(self.surface, rect, (200, 200, 200))

            ren = font.render(str(val), True, white)
            self.surface.blit(ren, (self.rect.right - ren.get_width(), y + ( dy-ren.get_height() )/2  ))

            ren = font.render(str(channel), True, white)
            self.surface.blit(ren, (self.rect.left + 10, y + ( dy-ren.get_height() )/2))

            y += dy
            prev = val
            x += ww
            # print ''


            # gfx.box(self.surface, self.rect,(255,200,100))
