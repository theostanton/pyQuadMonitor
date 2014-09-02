
import sys
print sys.version

import pygame
import pygame.time
from pygame import gfxdraw
from pygame.locals import *
from colors import *
gfx = pygame.gfxdraw

import Frame
import Graph
import Motor
import Dial

pygame.init()
font = pygame.font.Font(None, 20)
size = width, height = (1280, 800)
window = pygame.display.set_mode(size)
pygame.display.set_caption("Quad Monitor")
window.fill( black )
pygame.display.flip()

frames = []
frames.append( Frame.Frame(10,10,200,200,window,label='1',AR=Frame.FIXED_AR, empty_BG=True) )
frames.append( Frame.Frame(15,350,350,350,window,label='2') )
frames.append( Frame.Frame(500,250,350,350,window,AR=Frame.FIXED_AR,label='3') )

frames[0].add_element( Graph.Graph( window, 0, 'MDE', "Pitch" ) )
frames[0].add_element( Graph.Graph( window, 1, 'MDE', "ROLL" ) )
frames[0].add_element( Graph.Graph( window, 0, 'MDE', "Roll" ) )
frames[0].add_element( Graph.Graph( window, 0, 'MDE', "Roll" ) )

frames[1].add_element( Motor.Motor( window, 0, "A" ))
frames[1].add_element( Motor.Motor( window, 1, "B" ))
frames[1].add_element( Motor.Motor( window, 2, "C" ))
frames[1].add_element( Motor.Motor( window, 3, "D" ))

frames[2].add_element( Dial.Dial( window,0, 'AGM',"Pitch Measured"))
frames[2].add_element( Dial.Dial( window,1, 'AGM',"Roll Measured"))
frames[2].add_element( Dial.Dial( window,0, 'AGM',"Pitch Control"))
frames[2].add_element( Dial.Dial( window,1, 'AGM',"Roll Control"))

def main():
    full_mode = False
    global white
    while True:

        white = red

        if full_mode:
            for f in frames:
                f.draw_if_full()
        else :
            for f in frames:
                f.draw()


        for e in pygame.event.get():
            done = True
            if e.type == QUIT:
                sys.exit(0)

            elif e.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                ctrl_press = 0
                action = 0
                for i, f in enumerate(frames):
                    action = f.press(pos)
                    if action:
                        id = i
                        break

                if action:
                    print 'action', action, id
                    if action is Frame.KILL:
                        print 'remove ', id
                        frames.pop(id)

                    if action is Frame.FULL:
                        full_mode = frames[id].full
                        print 'full_mode', full_mode


            elif e.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for f in frames:
                    f.release(pos)
                
            elif e.type == MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                rel = pygame.mouse.get_rel()
                for f in frames:
                    if f.move_over( pos, rel ):
                        break

        update_window()

        pygame.time.wait(50)

def update_window():

    pygame.display.flip()
    window.fill( black )

if __name__ == '__main__':
    main()