# Mastermind - August 2020
# Arthur Jacquin (arthur@jacquin.xyz)
# https://github.com/arthur-jacquin/numworks-games

# Modules
from ion import keydown
from kandinsky import *
from random import randint

# Colors
COL = ((255, 63, 63), (255, 128, 0), (255, 255, 0), (46, 184, 46), (51, 153, 255), (153, 102, 255))

# Interface drawing
draw_string('MASTERMIND', 110, 5)
draw_string('Keys', 6+10, 35)
draw_string('Decoding board', 74+50, 35)
draw_string('Review', 6, 135+12)
for col in range(6):
    fill_rect(6+20*(col%3)+1, 55+20*(col > 2)+1, 18, 18, COL[col])
    draw_string(str(col+1), 6+20*(col%3)+5, 55+20*(col > 2)+1, (0,)*3, COL[col])
fill_rect(6+1, 95+1, 58, 18, (200,)*3)
draw_string('DEL', 6+15, 95+1, (0,)*3, (200,)*3)
fill_rect(6+1, 115+1, 58, 18, (200,)*3)
draw_string('EXE', 6+15, 115+1, (0,)*3, (200,)*3)

def wait(buttons): # Wait for keypress
    while True:
        for i in buttons:
            if keydown(i):
                while keydown(i): pass
                return i

while True:
    # Initialisation
    code = [randint(0,5) for i in range(4)]
    row = 0
    draw_string('Guess :', 80, 190)

    # Main loop
    while True:
        guess = []
        while True:
            k = wait((42, 43, 44, 36, 37, 38, 17, 52))
            if k == 52:
                if len(guess)!=4: continue
                break
            elif k == 17:
                if len(guess)==0: continue
                guess = guess[:-1]
                draw_string('  ', 160+20*len(guess), 190)
            else:
                if len(guess)==4: continue
                number = 1*(k==42)+2*(k==43)+3*(k==44)+4*(k==36)+5*(k==37)+6*(k==38)
                guess.append(number-1)
                fill_rect(142+20*len(guess), 191, 16, 16, COL[guess[-1]])
        draw_string(' '*8, 160, 190)
        for i in range(4): fill_rect(74+2+20*row, 55+20*i+2, 16, 16, COL[guess[i]])
        correct = sum([guess[i] == code[i] for i in range(4)])
        misplac, mirr = -1*correct, code[:]
        for i in range(4):
            if guess[i] in mirr:
                misplac += 1
                mirr.remove(guess[i])
        draw_string(str(misplac), 79+20*row, 137)
        draw_string(str(correct), 79+20*row, 157)
        if guess == code or row == 11:
            draw_string(' '*8, 80, 190)
            if guess == code: draw_string('You won in '+str(row+1)+' guesses !', 55, 180)
            else: draw_string('You lost !', 110, 180)
            draw_string('(Press OK to restart)', 55, 200)
            while not(keydown(4)): pass
            fill_rect(0, 180, 320, 40, (255,)*3)
            fill_rect(74, 55, 240, 120, (255,)*3)
            break
        else: row += 1
