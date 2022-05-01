# Pong - May 2022
# Arthur Jacquin (arthur@jacquin.xyz)
# https://github.com/arthur-jacquin/numworks-games

# Modules
from ion import keydown as kd
from kandinsky import draw_string, fill_rect
from time import sleep

# Colors
bg = (230,)*3
c1 = (238, 39, 51)
c2 = (78, 183, 72)
bl = (0,)*3

def init():
    global x, y, dx, dy, y1, dy1, s1, y2, dy2, s2
    x, y, dx, dy = 16, 106, 9, 0
    y1, dy1 = 73, 0
    y2, dy2 = 73, 0
    fill_rect(0, 0, 320, 222, bg)
    draw_string(str(s1), 135, 30, c1, bg)
    draw_string(str(s2), 175, 30, c2, bg)
    fill_rect(0, y1, 7, 75, c1)
    fill_rect(313, y2, 7, 75, c2)
    if max(s1, s2) < 5:
        sleep(1)
    else:
        while not(kd(4)): pass
        s1, s2 = 0, 0
    draw_string(" "*5, 135, 30, bg, bg)

def bar(x, y, dy, up, dw, c):
    dy = max(-21, min(dy + 4*(kd(dw)-kd(up)), 21))
    ny = max(0, min(y + dy, 147))
    if ny > y:
        fill_rect(x, y, 7, ny-y, bg)
        fill_rect(x, y+75, 7, ny-y, c)
    else:
        fill_rect(x, ny, 7, y-ny, c)
        fill_rect(x, ny+75, 7, y-ny, bg)
    return ny, dy*(ny != y)

def ball():
    global x, y, dx, dy, s1, s2
    fill_rect(x, y, 9, 9, bg)
    if x == 7:
        if y1-9 < y < y1+75+9:
            dx = 9
            dy = int((dy + dy1)/2)
        else:
            s2 += 1
            init()
    elif x == 304:
        if y2-9 < y < y2+75+9:
            dx = -9
            dy = int((dy + dy2)/2)
        else:
            s1 += 1
            init()
    x += dx
    if 0 <= y+dy <= 213:
        y += dy
    else:
        y = -dy-y+426*(dy>0)
        dy *= -1
    fill_rect(x, y, 9, 9, bl)

s1, s2 = 0, 0
init()
while True:
    y1, dy1 = bar(0, y1, dy1, 30, 36, c1)
    y2, dy2 = bar(313, y2, dy2, 34, 40, c2)
    ball()
    sleep(0.05)