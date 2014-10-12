from Element import *


class Key(Element):

    def __init__(self, surface):
        super(Key, self).__init__(surface)
        self.label = "Key"

    def draw(self):

        super(Key,self).draw()

        x = self.x
        y = self.y
        dy = self.rect.h / ( len(angle_labels) + len(motor_ids) + 2 )
        y += 2*dy

        for angle_id in angle_ids:
            ren = font.render(angle_labels[angle_id],True,colors[angle_id])
            self.surface.blit( ren, (x,y) )
            y += dy

        for motor_id in motor_ids:
            ren = font.render(motor_id.upper(),True,colors[motor_id])
            self.surface.blit( ren, (x,y) )
            y += dy


