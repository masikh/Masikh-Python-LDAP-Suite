#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 Robert Nagtegaal <masikh@gmail.com>
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

#
# NOTE:		  This code is based on an example found on the internet.
#		  Thus it resembles a strong similairity with the example.
#		  I believe it's 99% written by me. Unfortunally I could
#		  not find the example anymore on the internet. If this
#		  is a problem, rewrite this code. 


import curses,time
from os import system

def getmax(lines): return max([len(str(l)) for l in lines])

def scroller(screen,data,header):
    curses.start_color()
    curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
    wy=18
    wx=78
    offset = 4
    screen.addstr(19, 2, "[use arrow keys for scrolling or [ESC] for quit]", curses.color_pair(1))
    if type(data)==str:
        data = data.split('\n')

    padx = max(getmax(data),wx)
    pady = max(len(data),wy)
    max_x = padx-wx+2
    max_y = pady-wy

    pad = curses.newpad(pady,padx)

    for i,line in enumerate(data):
        pad.addstr(i,0,str(line))

    x=0
    y=0

    inkey=0
    while True:
	screen.refresh()
        pad.refresh(y,x,offset,2,wy+3,wx-1)
        inkey = screen.getch()
        if inkey=='KEY_UP':y=max(y-1,0)
        elif inkey==258:y=min(y+1,max_y)
        elif inkey==259:y=min(y-1,max_y)
        elif inkey==260:x=max(x-1,0)
        elif inkey==261:x=min(x+1,max_x)
        elif inkey==338:y=min(y+wy,max_y)
        elif inkey==339:y=max(y-wy,0)
        elif inkey==362:y=0
        elif inkey==385:y=max_y
	elif inkey==27:break
	elif inkey==263:break
	elif inkey==ord('q'):break

if __name__ == "__main__":
	print "call the function scroller(screen, data) for a program"
	print "this program is not a standalone program"
