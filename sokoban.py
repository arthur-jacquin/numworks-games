# Sokoban - June 2020
# Arthur Jacquin (arthur@jacquin.xyz)
# https://github.com/arthur-jacquin/numworks-games

# Modules
from ion import keydown
from kandinsky import *
from time import sleep

# Levels
LEVELS = ('4-5#10-|4-#3-#10-|4-#$--#10-|--3#--$##9-|--#--$-$-#9-|3#-#-##-#3-6#|#3-#-##-5#--..#|#-$--$10-..#|5#-3#-#@##--..#|4-#5-9#|4-7#8-',
    '12#--|#..--#5-3#|#..--#-$--$--#|#..--#$4#--#|#..4-@-##--#|#..--#-#--$-##|6#-##$-$-#|--#-$--$-$-$-#|--#4-#5-#|--12#',
    '8-8#-|8-#5-@#-|8-#-$#$-##-|8-#-$--$#--|8-##$-$-#--|9#-$-#-3#|#4.--##-$--$--#|##3.4-$--$3-#|#4.--10#|8#9-',
    '11-8#|11-#--4.#|12#--4.#|#4-#--$-$3-4.#|#-3$#$--$-#--4.#|#--$5-$-#--4.#|#-$$-#$-$-$8#|#--$-#5-#7-|##-9#7-|#4-#4-##7-|#5-$3-##7-|#--$$#$$--@#7-|#4-#4-##7-|11#8-',
    '8-5#4-|8-#3-5#|8-#-#$##--#|8-#5-$-#|9#-3#3-#|#4.--##-$--$3#|#4.4-$-$$-##-|#4.--##$--$-@#-|9#--$--##-|8-#-$-$--#-|8-3#-##-#-|10-#4-#-|10-6#-')

# Colors
BACK, TEXT = (120,)*3, (42,)*3 
COL = {
    '#': TEXT,           # Wall
    '@': (0, 153, 255),  # Player
    '+': (0, 122, 204),  # Player + Goal
    '$': (172, 115, 57), # Box
    '*': (134, 89, 45),  # Box + Goal
    '.': (70, 185, 70),  # Goal
    '-': BACK,           # Floor
    }

def wait(buttons = range(53)): # Wait for keypress 
    while True:
        for i in buttons:
            if keydown(i):
                sleep(0.1)
                return i

def decompress(rne): # Unpack the level
    grid = ['']
    while rne:
        if rne[0] == '|': grid.append('')
        elif 47 < ord(rne[0]) < 58:
            number = ''
            while 47 < ord(rne[0]) < 58: number += rne[0]; rne = rne[1:]
            grid[-1] += int(number)*rne[0]
        else: grid[-1] += rne[0]
        rne = rne[1:]
    return grid

def sett(x, y, test, valid, default):
    value = valid if grid[y][x] in test else default
    grid[y] = grid[y][:x] + value + grid[y][x+1:]
    fill_rect(X+d*x, Y+d*y, d, d, COL[value])

def win(): # Check for a win
    for y in grid:
        for char in y:
            if char=='$': return False
    return True

def menu(): # Rules, commands
    def display(*t):
        for i in list(range(len(t)))[::3]: draw_string(t[i], t[i+1], t[i+2], TEXT, BACK)
    fill_rect(0, 0, 320, 222, BACK)
    draw_string('SOKOBAN', 125, 6, TEXT, BACK)
    draw_string('Press a button to continue.', 25, 190, TEXT, BACK)
    display("You are a pusher employee in", 20, 40,
        "a store room.", 95, 60,
        "Push the boxes to their goal", 20, 90,
        "while minimizing moves.", 45, 110,
        "You can't push two boxes at", 20, 140,
        "once or pull them.", 70, 160)
    wait()
    fill_rect(0, 40, 320, 140, BACK)
    display("   COMMANDS       VISUALS", 25, 35,
        " Move : ARROWS    Wall :", 25, 60,
        " Undo : DEL     Player :", 25, 80,
        "Reset : EXE     + Goal :", 25, 100,
        " Help : ANS        Box :", 25, 120,
        "Level : +/-     + Goal :", 25, 140,
        " Quit : BACK      Goal :", 25, 160)
    for j in range(6): fill_rect(275, 60 + 20*j + 4, 10, 10, [COL['#'], COL['@'], COL['+'], COL['$'], COL['*'], COL['.']][j])
    wait()

menu()
count, i = len(LEVELS), 0
while True:
    # Initialisation
    grid, moves, his = decompress(LEVELS[i]), 0, ''
    
    # Interface drawing
    fill_rect(0, 0, 320, 222, BACK)
    draw_string('SOKOBAN', 125, 6, TEXT, BACK)
    lev = str(i+1) + '/' + str(count)
    draw_string(lev, 314-10*len(lev), 6, TEXT, BACK)
    draw_string('0', 6, 6, TEXT, BACK)
    X, Y, WIDTH, HEIGTH = 10, 33, 300, 180
    d = max(6, min(WIDTH//len(grid[0]), HEIGTH//len(grid), 12))
    X, Y = X + int((WIDTH - len(grid[0])*d)/2), Y + int((HEIGTH - len(grid)*d)/2)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            fill_rect(X+d*x, Y+d*y, d, d, COL[grid[y][x]])
            if grid[y][x] in '+@': XP, YP = x, y

    # Main loop
    while True:
        key = wait((0, 1, 2, 3, 4, 17, 45, 46, 51))
        if key in (0, 1, 2, 3, 17):
            if key == 17:
                if not(his): continue
                XN, YN = XP + (his[-1] in ('l', 'L')) - (his[-1] in ('r', 'R')), YP + (his[-1] in ('u', 'U')) - (his[-1] in ('d', 'D'))
                XN2, YN2 = 2*XP - XN, 2*YP - YN
            else:
                XN, YN = XP + (key==3) - (key==0), YP + (key==2) - (key==1)
                XN2, YN2 = 2*XN - XP, 2*YN - YP
                if (grid[YN][XN] == '#') or ((grid[YN][XN] in ('$', '*')) and (grid[YN2][XN2] in ('#', '$', '*'))): continue
                move = 'l'*(key==0) + 'u'*(key==1) + 'd'*(key==2) + 'r'*(key==3)
                if grid[YN][XN] in ('$', '*'): move = move.upper()
            
            if key != 17 or his[-1].islower(): sett(XP, YP, '+', '.', '-')
            else: sett(XP, YP, '+', '*', '$'); sett(XN2, YN2, '*', '.', '-')
            XP, YP = XN, YN
            if key != 17 and grid[YP][XP] in ('*', '$'): sett(XN2, YN2, '.', '*', '$')
            sett(XP, YP, '.*', '+', '@')
            
            moves = moves + 1 - 2*(key==17)
            his = his[:-1] if key==17 else (his + move)[-100:]
            draw_string(str(moves)+' ', 6, 6, TEXT, BACK)
            if win(): draw_string('YOU WON !', 115, 6, TEXT, BACK)
            continue
        elif key == 51: menu()
        else: i = (i + (key==45) - (key==46))%count
        break
