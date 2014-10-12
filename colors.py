colors = {}

angle_ids = ('A','G','M','D','E')
angle_labels = {}
angle_labels['A'] = 'Accelerometer'
angle_labels['G'] = 'Gyroscope'
angle_labels['M'] = 'Measured'
angle_labels['D'] = 'Desired'
angle_labels['E'] = 'Error'

motor_ids = ('a','b','c','d')
#motor_labels = {'A','B','C','D')

full = 200
half = 100

colors['A'] = (full, full, 0)
colors['G'] = (full, 0, full)
colors['M'] = (0, 0, full)
colors['D'] = (0, full, 0)
colors['E'] = (full, 0, 0)

colors['a'] = (full,half,0)
colors['b'] = (half,full,0)
colors['c'] = (full,0,half)
colors['d'] = (0,half,full)

black = 0, 0, 0
gray_10 = 10, 10, 10
white = 255, 255, 255, 60
white_40 = 255, 255, 255, 40
red = 255, 0, 0, 40
blue = 0, 255, 0, 40
green = 0, 0, 255, 40

frame_labels = ('Timings','Graphs','Timings','Key','PIDs','Dials')