from collections import defaultdict

# ##asdaa

a = 3

pid = {}
pid['a'] = [0, 0, 0, 0]
pid['b'] = [0, 0, 0, 0]
pid['c'] = [0, 0, 0, 0]
pid['d'] = [0, 0, 0, 0]

angle_log = defaultdict(list)
angles = {}
for key in 'AGMDE':
    angles[key] = [0, 0, 0]
    angle_log[key] = []
    angle_log[key].append([0, 0, 0])
    angle_log[key].append([0, 0, 0])
    angle_log[key].append([0, 0, 0])
    angle_log[key].append([0, 0, 0])

rx = []
timings = []
timingsLabels = ['Loop', 'Sensors', 'Motor', 'RX', 'Serial']
ratios = []


def set_pid(motor, vals):
    pid[motor] = []
    tot = 0
    for v in vals:
        pid[motor].append(v / 500)
        # tot += v / 500
        # pid[motor].append(tot)


def set_angle(angleid, vals):
    # if angleid is 'M': print 'MM!'
    angles[angleid] = vals
    angle_log[angleid].append(vals)
    if len(angle_log[angleid]) > 1000:
        angle_log[angleid].pop(0)


def set_rx(vals):
    global rx
    rx = vals


def set_timings(vals):
    global timings
    print timings
    timings = vals


def set_ratios(vals):
    global ratios
    ratios = vals