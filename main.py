import sys

import Slider


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
import dial
import RX
import Timings

import Data

import serial

connected = False
try:
    # ser = serial.Serial('/dev/tty.Quad-DevB', 115200)
    ser = serial.Serial('/dev/cu.usbmodem1a12451', 115200)
    print 'connected'
    connected = True
except:
    print 'no connect'

pygame.init()

size = width, height = (1280, 780)

if False:
    window = pygame.display.set_mode(size, FULLSCREEN)
else:
    window = pygame.display.set_mode(size)

pygame.display.init()

font = pygame.font.Font(None, 20)
# window = pygame.display.set_mode(size)
pygame.display.set_caption("Quad Monitor")
window.fill(black)
pygame.display.flip()

frames = []
frames.append(Frame.Frame(10, 10, 200, 200, window, label='1'))
frames.append(Frame.Frame(15, 350, 350, 350, window, AR=Frame.FIXED_AR, label='2'))
frames.append(Frame.Frame(500, 250, 350, 350, window, AR=Frame.FIXED_AR, label='3'))
frames.append(Frame.Frame(200, 250, 350, 350, window, label='4'))
frames.append(Frame.Frame(200, 100, 200, 200, window, label='5', layout=Frame.VERT))
frames.append(Frame.Frame(300, 300, 200, 200, window, label='6', layout=Frame.VERT))

frames[0].add_element(Graph.Graph(window, 0, 'MDE', "Roll"))
frames[0].add_element(Graph.Graph(window, 1, 'MDE', "Pitch"))
frames[0].add_element(Graph.Graph(window, 0, 'MAG', "Roll"))
frames[0].add_element(Graph.Graph(window, 1, 'MAG', "Pitch"))

# frames[0].add_element(Graph.Graph(window, 0, 'M', "Roll Measured"))
# frames[0].add_element(Graph.Graph(window, 0, 'AG', "Roll Gyro and Acc"))
# frames[0].add_element(Graph.Graph(window, 0, 'G', "Roll Gyro"))
# frames[0].add_element(Graph.Graph(window, 0, 'A', "Roll Acc"))

frames[1].add_element(Motor.Motor(window, "a", "A"))
frames[1].add_element(Motor.Motor(window, "b", "B"))
frames[1].add_element(Motor.Motor(window, "d", "D"))
frames[1].add_element(Motor.Motor(window, "c", "C"))

frames[2].add_element(dial.Dial(window, 1, 'AGM', "Pitch Measured"))
frames[2].add_element(dial.Dial(window, 0, 'AGM', "Roll Measured"))
frames[2].add_element(dial.Dial(window, 1, 'MDE', "Pitch Control"))
frames[2].add_element(dial.Dial(window, 0, 'MDE', "Roll Control"))

frames[3].add_element(RX.RX(window))

frames[4].add_element(Slider.Slider(window, label="KP"))
frames[4].add_element(Slider.Slider(window, label="KI"))
frames[4].add_element(Slider.Slider(window, label="KD"))
frames[4].add_element(Slider.Slider(window, label="Comp"))

frames[5].add_element(Timings.Timings(window))


def main():
    full_mode = False
    global white
    running = True
    while running:

        white = red

        if full_mode:
            for f in frames:
                f.draw_if_full()
        else:
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
                    if f.move_over(pos, rel):
                        break

            elif e.type == KEYDOWN:
                keydown(e.key)

            elif e.type == QUIT:
                print 'quit'
                running = False
                sys.exit(0)

        update_window()

        while connected and ser.inWaiting():
            # print 'got', ser.inWaiting()
            get_serial(ser.readline())

        pygame.time.wait(50)


def get_serial(line):
    # print 'line', line

    try:

        if line[0] is ' ':
            print line[1:]
            return

        else:
            vals = line.split(',')

            if vals[0] is '':
                print 'return', vals
                return

            if vals[0] in 'AGMDE':
                # global angles
                Data.set_angle(vals[0], map(int, vals[1:]))
                #
                # if len( logs[vals[0]] ) > 1024:
                # logs[vals[0]].pop(0)
                #
                # logs[vals[0]].append( map( int, vals[1:] ) )

            elif vals[0] in 'T':
                Data.set_timings(map(int, vals[1:]))

            elif vals[0] in 'P':
                Data.set_ratios(map(float, vals[1:]))

            elif vals[0] in 'R':
                Data.set_rx(map(int, vals[1:]))

            elif vals[0] in 'abcd':
                global motors
                Data.set_pid(vals[0], map(int, vals[1:]))
                # motors[vals[0]].put(map( int,vals[1:]) )
            else:
                print 'line', line,
    except Exception as e:

        print 'serial error'
        print e.message
        print 'serial error'


def keydown(key):
    print 'keydown',
    print key
    if key == K_LEFT:
        shift_full('LEFT')
    elif key == K_RIGHT:
        shift_full('RIGHT')


def shift_full(direction):
    global full_mode
    full_mode = True

    for i, f in enumerate(frames):
        if f.full:
            f.toggle_full()

            if 'RIGHT' in direction:

                if i + 1 < len(frames):
                    frames[i + 1].toggle_full()
                else:
                    frames[0].toggle_full()
            else:
                if i - 1 >= 0:
                    frames[i - 1].toggle_full()
                else:
                    frames[len(frames) - 1].toggle_full()

            break
            # try:
            # frames[i+dir].toggle_full()
            # except:
            # if dir:
            # frames[dir].toggle_full()
            # break
    else:
        print 'set first'
        frames[0].toggle_full()


def update_window():
    pygame.display.flip()
    window.fill(black)


if __name__ == '__main__':
    main()