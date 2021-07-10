# Tetris - December 2020
# Arthur Jacquin (arthur@jacquin.xyz)
# https://github.com/arthur-jacquin/numworks-games

# Modules
from ion import keydown
from kandinsky import draw_string, fill_rect
from time import monotonic, sleep
from random import randint

# Tools
Xdom, Ydom = range(10), range(21)
commands = ('Move     ARROWS', 'Rotate   ()', 'Replay   OK', 'Quit     BACK')
TYPES = (
    (((-1, 1), (0, 1), (1, 0)), ((-1, -1), (-1, 0), (0, 1))), # Red (Z)
    (((-1, 0), (1, 0), (1, 1)), ((1, -1), (0, -1), (0, 1)), ((-1, -1), (-1, 0), (1, 0)), ((-1, 1), (0, 1), (0, -1))), # Orange (L)
    (((0, 1), (1, 0), (1, 1)),), # Yellow (O)
    (((-1, 0), (0, 1), (1, 1)), ((0, 1), (1, 0), (1, -1))), # Green (S)
    (((-1, 0), (1, 0), (2, 0)), ((0, -1), (0, 1), (0, 2))), # Light blue (I)
    (((-1, 0), (0, 1), (1, 0)), ((0, 1), (1, 0), (0, -1)), ((-1, 0), (0, -1), (1, 0)), ((0, -1), (-1, 0), (0, 1))), # Magenta (T)
    (((-1, 1), (-1, 0), (1, 0)), ((0, -1), (0, 1), (1, 1)), ((-1, 0), (1, 0), (1, -1)), ((-1, -1), (0, -1), (0, 1)))) # Dark blue (J)

# Colors
COL = (
    (255,)*3, # NOT BLOCK - Background
    (0,)*3, # NOT BLOCK - Text
    (238, 39, 51), # Red (Z)
    (248, 150, 34), # Orange (L)
    (253, 225, 0), # Yellow (O)
    (78, 183, 72), # Green (S)
    (43, 172, 226), # Light blue (I)
    (146, 43, 140), # Magenta (T)
    (0, 90, 157)) # Dark blue (J)

def sett(X, Y, TYPE):
    M[Y] = M[Y][:X] + str(TYPE) + M[Y][X+1:]
    if TYPE == 1: fill_rect(210+11*X, 211-11*Y, 9, 9, COL[int(tetro[2])+2])
    else: fill_rect(210+11*X, 211-11*Y, 9, 9, COL[TYPE])

def unpack(op = False):
    X, Y, TYPE, ORIENTATION = tetro
    if op == 'down': Y -= 1
    elif op == 'left': X -= 1
    elif op == 'right': X += 1
    elif op == 'rot_right': ORIENTATION = (ORIENTATION + 1)%len(TYPES[TYPE])
    elif op == 'rot_left': ORIENTATION = (ORIENTATION - 1)%len(TYPES[TYPE])
    cases = [[X, Y]]
    for case in TYPES[TYPE][ORIENTATION]: cases.append([X + case[0], Y + case[1]])
    return cases, [X, Y, TYPE, ORIENTATION]     

def form(op = False):
    if op:
        old, _ = unpack()
        new, newtetro = unpack(op)
    else: new, _ = unpack()
    for case in new:
        if not(case[0] in Xdom) or case[1] < 0 or int(M[case[1]][case[0]]) > 1: return False
    if op:
        for case in old: sett(case[0], case[1], 0)
    for case in new: sett(case[0], case[1], 1)
    return newtetro

def sample(): # 7-bag random generator
    indexes, res = list(range(7)), []
    for i in range(7):
        k = randint(0, 6-i)
        res.append(indexes.pop(k))
    return res

# Interface drawing
fill_rect(0, 0, 320, 222, COL[0])
fill_rect(207, 0, 1, 222, COL[1])
draw_string('Next', 133, 20, COL[1], COL[0])
draw_string('Lines', 28, 93, COL[1], COL[0])
for string in commands: draw_string(string, 28, 130 + 20*commands.index(string), COL[1], COL[0])
fill_rect(28, 20, 72, 24, COL[-1])
fill_rect(52, 44, 24, 24, COL[-1])
fill_rect(30, 22, 68, 20, COL[0])
fill_rect(54, 42, 20, 24, COL[0])
for i in range(6): draw_string('TETRIS'[i], 28+3+11*i, 20+4, COL[i+2], COL[0])
draw_string('NW', 54, 48, (100,)*3, COL[0])

while True:
    # Initialisation
    lines, M, bag = 0, ['0'*len(Xdom),]*len(Ydom), sample()
    time = monotonic()
    fill_rect(208, 0, 112, 222, COL[0])
    draw_string('0'+' '*7, 118, 93, COL[1], COL[0])

    # Main loop
    while True:
        if len(bag) < 2: bag += sample()
        last = tetro = [4, 19, bag[0], 0]
        bag.pop(0)
        if not(form(tetro)): break
        fill_rect(131, 42, 44, 22, COL[0])
        for case in [(0, 0)] + list(TYPES[bag[0]][0]): fill_rect(148+11*case[0]-5*(bag[0] in (2, 4)), 43 + 11*(1-case[1]), 9, 9, COL[bag[0]+2])
        while True: 
            # Time and movement gestion
            while monotonic() < time + 0.2 + .5/(lines+2):
                if keydown(2): break
                elif keydown(34): tetro = form('rot_right')
                elif keydown(33): tetro = form('rot_left')
                elif keydown(0): tetro = form('left')
                elif keydown(3): tetro = form('right')
                if tetro != last:
                    sleep(0.15)
                    if tetro: last = tetro
                    else: tetro = last
            time = monotonic()
            sleep(0.03)
            newtetro = form('down')
            if newtetro: last = tetro = newtetro
            else:
                for Y in Ydom:
                    for X in Xdom:
                        if M[Y][X] == '1': sett(X, Y, int(tetro[2])+2)
                completed = False
                for line in M[:]:
                    if not('0' in line): # Full row
                        M.remove(line)
                        M.append('0'*len(Xdom))
                        lines += 1
                        completed = True
                if completed: # Full refresh
                    sleep(0.1)
                    draw_string(str(lines), 118, 93, COL[1], COL[0])
                    for Y in Ydom:
                        for X in Xdom: sett(X, Y, int(M[Y][X]))
                break
    while not(keydown(4)): pass
