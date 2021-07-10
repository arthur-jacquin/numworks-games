# Snake - April 2020
# Arthur Jacquin (arthur@jacquin.xyz)
# https://github.com/arthur-jacquin/numworks-games

# Modules
from ion import keydown
from kandinsky import *
from time import monotonic
from random import choice

# Parameters, tools
speed, add = 0.15, 15
mode = "classic" # "classic" or "mad"
borders = "solid" # "solid" or "teleportation"

# Colors
back = (255,255,255) # Background
imp = (0,0,0) # Title, borders, menus
sub = (70,70,70) # Score
body = (0, 204, 0) # Snake body
bord = (0, 104, 0) # Snake border
red = (248, 0, 0) # Tongue, eyes, apples
red_dark = (200, 0, 0) # Apples

def wait(buttons = range(53)): # Wait for keypress
    while True:
        for i in buttons:
            if keydown(i):
                while keydown(i): pass
                return i 

def pom(): # Draw an apple
    up = [choice(range(32)), choice(range(20))]
    while get_pixel(10*up[0], 22 + 10*up[1]) == bord:
        up = [choice(range(32)), choice(range(20))]
    Xp, Yp = 10*up[0], 22 + 10*up[1]
    fill_rect(Xp,Yp+4,10,4,red_dark)
    fill_rect(Xp+2,Yp+2,6,8,red_dark)
    fill_rect(Xp+1,Yp+3,8,6,red)
    set_pixel(Xp+1,Yp+3,red_dark)
    set_pixel(Xp+1,Yp+8,red_dark)
    set_pixel(Xp+8,Yp+3,red_dark)
    set_pixel(Xp+8,Yp+8,red_dark)
    fill_rect(Xp+2,Yp,3,1,bord)
    fill_rect(Xp+1,Yp+1,5,1,bord)
    fill_rect(Xp+2,Yp+1,2,1,body)
    fill_rect(Xp+3,Yp+2,3,1,body)

while True:
    # Initialisation
    di, sn = 3, [30, 52, 80, 52] # Direction, snake tail and head coordinates
    score = to_add = 0 # Score, growth
    time = monotonic() # Time
    
    # Interface drawing
    fill_rect(0,0,320,222,back) # Clearing
    fill_rect(0,21,320,1,imp) # Upper border
    draw_string("SNAKE",135,2,imp) # Title
    draw_string("0",304,2,sub) # Score
    fill_rect(30,52,60,10,bord) # Initial snake
    fill_rect(31,53,58,8,body)
    if mode == "classic": pom()
    
    # Main loop
    while True:
        # Direction and time gestion
        direction = di 
        while monotonic() < time + speed:
            for k in range(4):
                if keydown(k) and direction+k != 3: di = k
        time = monotonic()
        
        # Tail refresh
        if int(to_add): to_add -= 1
        else:
            if get_pixel(sn[0],sn[1]+1) == body: sens = 0
            elif get_pixel(sn[0]+9,sn[1]+1) == body: sens = 3
            elif get_pixel(sn[0]+1,sn[1]) == body: sens = 1
            elif get_pixel(sn[0]+1,sn[1]+9) == body: sens = 2
            fill_rect(sn[0],sn[1],10,10,back)
            sn[0], sn[1] = (sn[0] + 10*(sens==3) - 10*(sens==0))%320, (sn[1] + 10*(sens==2) - 10*(sens==1)-22)%200+22
            if sens == 0: fill_rect(sn[0]+9,sn[1],1,10,bord)
            elif sens == 3: fill_rect(sn[0],sn[1],1,10,bord)
            elif sens == 1: fill_rect(sn[0],sn[1]+9,10,1,bord)
            elif sens == 2: fill_rect(sn[0],sn[1],10,1,bord)
        
        # Head refresh - part 1
        fill_rect(sn[2]+1,sn[3]+1,8,8,body)
        if di == 0: fill_rect(sn[2],sn[3]+1,1,8,body)
        elif di == 1: fill_rect(sn[2]+1,sn[3],8,1,body)
        elif di == 3: fill_rect(sn[2]+9,sn[3]+1,1,8,body)
        elif di == 2: fill_rect(sn[2]+1,sn[3]+9,8,1,body)
        sn[2], sn[3] = sn[2] + 10*(di==3) - 10*(di==0), sn[3] + 10*(di==2) - 10*(di==1)
        if borders == "teleportation": sn[2], sn[3] = sn[2]%320, (sn[3]-22)%200 + 22
        
        # Treatment
        if get_pixel(sn[2], sn[3]) == bord or not(sn[2] in range(320)) or not(sn[3] in range(22, 222)): break # Encounters
        if get_pixel(sn[2] + 4,sn[3] + 4) == red: # New apple
            score += 15
            to_add += add
            pom()
        
        # Head refresh - part 2
        fill_rect(sn[2],sn[3],10,10,bord)
        fill_rect(sn[2]+1,sn[3]+1,8,8,body)
        if di == 0:
            fill_rect(sn[2]+4,sn[3]+2,1,6,bord)
            fill_rect(sn[2]+3,sn[3]+3,1,4,red)
            fill_rect(sn[2]+3,sn[3]+4,2,2,body)
            fill_rect(sn[2]+9,sn[3]+1,1,8,body)
        elif di == 1:
            fill_rect(sn[2]+2,sn[3]+4,6,1,bord)
            fill_rect(sn[2]+3,sn[3]+3,4,1,red)
            fill_rect(sn[2]+4,sn[3]+3,2,2,body)
            fill_rect(sn[2]+1,sn[3]+9,8,1,body)
        elif di == 3:
            fill_rect(sn[2]+5,sn[3]+2,1,6,bord)
            fill_rect(sn[2]+6,sn[3]+3,1,4,red)
            fill_rect(sn[2]+5,sn[3]+4,2,2,body)
            fill_rect(sn[2],sn[3]+1,1,8,body)
        elif di == 2:
            fill_rect(sn[2]+2,sn[3]+5,6,1,bord)
            fill_rect(sn[2]+3,sn[3]+6,4,1,red)
            fill_rect(sn[2]+4,sn[3]+5,2,2,body)
            fill_rect(sn[2]+1,sn[3],8,1,body)
            
        # Final treatment
        score += speed
        draw_string("  "+str(int(score)),int(314-10*len("  "+str(int(score)))),2,sub) # Score refresh
        if mode == "mad":
            if speed > 0.04: speed *= 0.99
            to_add += 0.2

    # Lose
    draw_string("YOU LOST !",110,2,(255,0,0))
    while not(keydown(4)): pass
