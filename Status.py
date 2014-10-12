from Element import *


class Status(Element):

    def __init__(self, surface):
        super(Status, self).__init__(surface)
        self.option_rects = []

        x = self.x
        y = self.y
        dy = self.rect.h / len(frame_labels)

        for frame_label in frame_labels:
            ren = font.render(frame_label,True,white_40)
            self.surface.blit( ren, (x,y) )
            y += dy
            rect = ren.get_rect()
            rect.move(x,y)
            self.option_rects.append( rect )

    def draw(self):

        x = self.x
        y = self.y
        dy = self.rect.h / len(frame_labels)

        for frame_label in frame_labels:
            ren = font.render(frame_label,True,white_40)
            self.surface.blit( ren, (x,y) )
            y += dy

