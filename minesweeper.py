# Minesweeper - April 2020
# Arthur Jacquin (arthur@jacquin.xyz)
# https://github.com/arthur-jacquin/numworks-games

''' Codes   | Mine |            Not a mine                |
|  Covered  |   9  |  0 to  8 (nb of adjacent mines)      |
| Uncovered |  19  | 10 to 18 (nb of adjacent mines + 10) |
|  Flagged  |  19  | 20 to 28 (nb of adjacent mines + 20) |
'''

# Modules
from ion import keydown
from kandinsky import set_pixel, draw_string, fill_rect
from random import choice

# Parameters, tools
mines = 20
Xdomain, Ydomain = range(16), range(10) # Grid dimensions
prox = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

# Colors
imp = (0,0,0) # Title, cursor, content
grey = (70,70,70) # Text, borders
light = (220,220,220) # Unknown boxes
none = (255,255,255) # Empty boxes, background
curs = (0,0,255) # Cursor
numb = ((0,0,255),(0,127,0),(255,0,0),(0,0,127),(127,0,0),(0,127,127),(0,0,0),(127,127,127)) # Numbers

def wait(buttons = range(53)): # Wait for keypress
    while True:
        for i in buttons:
            if keydown(i):
                while keydown(i): pass
                return i 

def mine(x,y,b,a): # Draw a mine
    fill_rect(x+2+4,y+2+4,9,9,b)
    fill_rect(x+4,y+6+4,13,1,b)
    fill_rect(x+6+4,y+4,1,13,b)
    fill_rect(x+4+4,y+4+4,2,2,(255,255,255))
    for p in [[9,2],[10,3],[10,9],[9,10],[3,10],[2,9],[2,3],[3,2]]:
        set_pixel(x+p[0]+4,y+p[1]+4,a)

def case(X,Y): # Draw a box
    value = MAT[Y][X]
    x, y = 20*X, 20*Y + 22
    fill_rect(x,y,20,20,grey) # Borders
    if value < 10: # Unknown
        fill_rect(x+1,y+1,18,18,light)
    elif value == 10: # Empty
        fill_rect(x+1,y+1,18,18,none)
    elif value in range(11,19): # Number
        fill_rect(x+1,y+1,18,18,none)
        draw_string(str(value-10),x+5,y+1,numb[value-11])
    elif value == 19: # Uncovered mine
        fill_rect(x+1,y+1,18,18,(255,0,0))
        mine(x,y,imp,(255,0,0))
    elif value > 19: # Flag
        fill_rect(x+1,y+1,18,18,light)
        fill_rect(x+10,y+8,2,6,imp)
        fill_rect(x+6,y+14,8,2,imp)
        fill_rect(x+6,y+4,6,4,(255,0,0))
    if cursor == [X,Y]: # Cursor
        fill_rect(x,y,20,3,curs)
        fill_rect(x,y,3,20,curs)
        fill_rect(x,y+17,20,3,curs)
        fill_rect(x+17,y,3,20,curs)

def search(old): # Search around for empty boxes
    new = []
    for i in old:
        for p in prox:
            tX, tY = i[0]+p[0], i[1]+p[1]
            if tX in Xdomain and tY in Ydomain:
                if MAT[tY][tX] == 0: new.append([tX,tY])
                if not(MAT[tY][tX] in range(10,19)):
                    MAT[tY][tX] = (MAT[tY][tX])%10 + 10
                    case(tX,tY)
    if new != []: search(new)

while True:
    # Initialisation
    compteur = mines # Displayed discovered mines count
    decouv = 0 # Real count
    cursor = [8,5] # Cursor coordinates
    MAT = [[0]*len(Xdomain)]*len(Ydomain) # Empty matrix
    
    # Interface drawing
    draw_string("MINESWEEPER",105,2,imp)
    draw_string((" "+str(compteur)+"/"+(str(mines)+" ")[:2])[-5:],265,2,grey)
    mine(245,0,grey,none)
    fill_rect(0,21,320,1,grey)
    for Y in Ydomain:
        for X in Xdomain: case(X,Y)
    
    # Main loop
    while True:
        X, Y = cursor
        result = wait([0,1,2,3,4,17]) # Get keypress
        if result < 4: # Cursor movement
            if result==0 and cursor[0]-1 in Xdomain: cursor[0] -= 1
            elif result==1 and cursor[1]-1 in Ydomain: cursor[1] -= 1
            elif result==2 and cursor[1]+1 in Ydomain: cursor[1] += 1
            elif result==3 and cursor[0]+1 in Xdomain: cursor[0] += 1
            case(X,Y)
            case(cursor[0],cursor[1])
        elif result == 4: # Mine clearance
            if MAT == [[0]*len(Xdomain)]*len(Ydomain): # Matrix generation
                bombes = []
                for i in range(mines):
                    x, y = choice(Xdomain), choice(Ydomain)
                    while (x,y) in bombes or (x,y) == (X,Y):
                        x, y = choice(Xdomain), choice(Ydomain)
                    bombes.append((x,y))
                MAT = []
                for y in Ydomain:
                    column = []
                    for x in Xdomain:
                        if (x,y) in bombes: column.append(9)
                        else: column.append(sum([1*((x+t[0],y+t[1]) in bombes) for t in prox]))
                    MAT.append(column)
            if MAT[Y][X] > 19:
                compteur += 1
                draw_string((" "+str(compteur))[-2:],265,2,grey)
            if MAT[Y][X] in range(11,19): # Automated mine clearance
                while True:
                    flags = 0
                    for t in prox:
                        if X+t[0] in Xdomain and Y+t[1] in Ydomain:
                            if MAT[Y+t[1]][X+t[0]] == 9: break
                            elif MAT[Y+t[1]][X+t[0]] == 29: flags += 1
                    if MAT[Y][X]-10 == flags:
                        for t in prox:
                            if X+t[0] in Xdomain and Y+t[1] in Ydomain and MAT[Y+t[1]][X+t[0]]<9:
                                MAT[Y+t[1]][X+t[0]] = (MAT[Y+t[1]][X+t[0]])%10+10
                                case(X+t[0],Y+t[1])
                                if MAT[Y+t[1]][X+t[0]]==10: search([[X+t[0],Y+t[1]]])
                    break
            MAT[Y][X] = (MAT[Y][X])%10 + 10
            case(X,Y)
            if MAT[Y][X] == 10: search([[X,Y]]) # Automated search
            elif MAT[Y][X] == 19: # Lose
                for x in Xdomain:
                    for y in Ydomain:
                        if (MAT[y][x])%10 == 9: # Reveal the mines
                            MAT[y][x] = 19
                            case(x,y)
                        elif MAT[y][x] > 19: # Strike misplaced flags
                            for i in range(18):
                                fill_rect(20*x+i,20*y+23+i,3,1,imp)
                                fill_rect(20*x+17-i,20*y+23+i,3,1,imp)
                fill_rect(0,0,320,21,none)
                draw_string("YOU LOST !",110,2,(255,0,0))
                break
        elif result == 17: # (Un)Flagging
            if MAT[Y][X] < 20: sens = 1
            else: sens = -1
            compteur -= sens
            if (MAT[Y][X])%10 == 9: decouv += sens
            MAT[Y][X] = (MAT[Y][X])%10 + 20*(sens==1)
            draw_string((" "+str(compteur))[-2:],265,2,grey)
            case(X,Y)
        if compteur == 0 and decouv == mines: # Win
            for x in Xdomain:
                for y in Ydomain:
                    if MAT[y][x]<9:
                        MAT[y][x] = (MAT[y][x])%10+10
                        case(x,y)
            fill_rect(0,0,320,21,none)
            draw_string("YOU WON !",115,2,(0,153,0))
            cursor = [42,120]
            case(X,Y)
            break
    while not(keydown(4)): pass
