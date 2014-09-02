import pygame
import pygame.time
import sys
from pygame.locals import *
from pygame import gfxdraw
gfx = pygame.gfxdraw
from collections import defaultdict
from colors import *

import dial
import Motor
import Graph
import Slider


import serial
try :
    ser = serial.Serial('/dev/cu.usbmodem1a12431', 115200)
except:
    'no connect'

ROLL = 0
PITCH = 1
YAW = 2

pygame.init()
font = pygame.font.Font(None, 20)
size = width, height = (1280, 800)
window = pygame.display.set_mode(size)
window.fill( black )
pygame.display.flip()


r_dial = width / 8
pitch_dial      = dial.Dial( 0, 0, r_dial, PITCH, 'AGM',"Pitch Measured" )
roll_dial       = dial.Dial( 2*r_dial,   0, r_dial, ROLL, 'AGM',"Roll Measured" )
pitch_ctrl_dial = dial.Dial( 0, 2*r_dial, r_dial, PITCH, 'MDE',"Pitch Control" )
roll_ctrl_dial  = dial.Dial( 2*r_dial, 2*r_dial, r_dial, ROLL, 'MDE',"Roll Control" )

dials = (pitch_dial,pitch_ctrl_dial,roll_ctrl_dial,roll_dial)

motors_x = width / 2
motors_y = 0
motors_d = width / 4

motors = {}
motors['a'] = Motor.Motor( motors_x, motors_y, motors_d, 'A' )
motors['b'] = Motor.Motor( motors_x+motors_d, motors_y, motors_d, 'B' )
motors['c'] = Motor.Motor( motors_x, motors_y+motors_d, motors_d, 'C' )
motors['d'] = Motor.Motor( motors_x+motors_d, motors_y+motors_d, motors_d, 'D' )

graph_x = 0
graph_y = 4 * r_dial
graph_w = width / 3
graph_h = height - graph_y
graphs = []
graphs.append( Graph.Graph( graph_x,graph_y, graph_w, graph_h, PITCH, 'MDE', "Pitch" ) )
graphs.append( Graph.Graph( graph_x + graph_w, graph_y, graph_w, graph_h, ROLL, 'MDE', "Roll" ) )

sliders_x = width - width / 3
sliders_y = graph_y
sliders_w = graph_w - 100
sliders_h = graph_h / 3

sliders = []

sliders.append( Slider.Slider( sliders_x, sliders_y,               sliders_w, sliders_h, 'P', 1000) )
sliders.append( Slider.Slider( sliders_x, sliders_y + sliders_h,   sliders_w, sliders_h, 'I', 1000) )
sliders.append( Slider.Slider( sliders_x, sliders_y + 2*sliders_h, sliders_w, sliders_h, 'D', 1000) )


keys = ('A','G','M','D','E')
key_labels = ('Accel','Gyro','Measured','Desired','Error')

logs = defaultdict(list)
angles = {}
for k in keys:
    angles[k] = [0,0,0]
    logs[k] = []

 # = (  accel, gyro, mes, des, err )

def main():
    fresh = True
    drag = False
    while True:
        no_connect = True
        print 'tick'
        while no_connect or not ser.inWaiting():
            print 'tock'
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit(0)
                elif e.type == MOUSEBUTTONDOWN:
                    print 'mouse down'
                    drag = True
                    pos = pygame.mouse.get_pos()
                    for s in sliders:
                        s.isover(pos)

                    #send_serial()
                    break
                elif e.type == MOUSEMOTION and drag:
                    pos = pygame.mouse.get_pos()
                    break
                elif e.type == MOUSEBUTTONUP:
                    drag = False
                    pos = pygame.mouse.get_pos()
                    for s in sliders:
                        over = s.isover(pos)
                        if over:
                            send_serial(over)
                            #print 'id', id, 'val', val
            if no_connect:
                break
            pygame.time.wait(10)

        while not no_connect and ser.inWaiting():
            get_serial( ser.readline() )

        for m in motors.itervalues():
            m.draw(window)

        for d in dials:
            d.draw(window,angles,motors)

        for g in graphs:
            g.draw(window, logs)

        for s in sliders:
            s.draw(window)



        update_window()

def send_serial(over):
    id, val = over
    ser.write(id)
    ser.write(str(val))

def get_serial( line ):

    #print vals

    if line[0] is ' ':
        print line[1:]
        return

    else :
        vals = line.split(',')

        if vals[0] is '':
            print 'return', vals
            return

        if vals[0] in 'AGMDE':
            global angles
            angles[vals[0]] = map( int, vals[1:] )

            if len( logs[vals[0]] ) > 1024:
                logs[vals[0]].pop(0)

            logs[vals[0]].append( map( int, vals[1:] ) )

        elif vals[0] in 'abcd':
            global motors
            motors[vals[0]].put(map( int,vals[1:]) )

def update_window():
    draw_key()
    pygame.display.flip()
    window.fill( black )

def draw_key():
    h = 100
    w = 100
    x = width - w
    y = height - h
    # gfx.line(window,x,y,x,height,white)
    # gfx.line(window,x,y,width,y,white)

    pad = 10
    ygap = h - 2 * pad
    ygap /= len(key_labels)

    x += pad
    y += pad

    for key,label in zip(keys,key_labels):
        ren = font.render(label,True,colors[key])
        window.blit(ren,(x,y))
        y += ygap

if __name__ == '__main__':
    main()