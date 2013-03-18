#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 Robert Nagtegaal <masikh@gmail.com>
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import curses,os,re,time
import helper_apply_ldif as apply_ldif

# Open the file 'fname' and return its contents and error state.
def openfile(selection):
	fname = selection
        error = "OK"
        content = "" 
        try:
                with open(fname) as f:
                        fcontent = f.readlines()
                        for line in fcontent:
                                content += line 
                f.close()
        except:
                error = 'Something is wrong! (e.g. File does not exist!)'
        return error,content

def showSelection(s, env, content):
	length = width = 0 
	temp = content
	for i in temp.split('\n'):
		length +=1
		if len(i) > width:width = len(i)
	
	width += 9 
	mypad = curses.newpad(length, width)
	mypad_posx = mypad_posy = 0
	s.erase()
	s.box()
	s.hline(19, 2, curses.ACS_HLINE, 70)
	s.hline(1, 1, curses.ACS_HLINE, 76)
	s.hline(18, 1, curses.ACS_HLINE, 76)
	s.addstr(19,2,"[Use [ESC] to abort and [ARROWS] to scroll]",curses.color_pair(1))
	s.refresh()
	while True:
		mypad.refresh(mypad_posy, mypad_posx, 5, 3, 20, 76)
		i = 0 
		for line in content.split('\n'):
			mypad.addstr(i, 0, "%s"%(line), curses.color_pair(2))
			i += 1
			mypad.refresh(mypad_posy, mypad_posx, 5, 3, 20, 76)
		x = s.getch()
		# Down arrow (scroll down in text)
		if x == 258:
			if mypad_posy < length - 19:mypad_posy += 1
			mypad.refresh(mypad_posy, mypad_posx, 5, 3, 20, 76)
		# Up arror (scroll up in text)
		if x == 259 and mypad_posy > 0:
			mypad_posy -= 1
			mypad.refresh(mypad_posy, mypad_posx, 5, 3, 20, 76)
		if  x == 260 and mypad_posx > 0:
			mypad_posx -= 1
			mypad.refresh(mypad_posy, mypad_posx, 5, 3, 20, 76)
		if x == 261 and mypad_posx < width - 80:
			mypad_posx += 1
			mypad.refresh(mypad_posy,mypad_posx, 5, 3, 20, 76)
		if x == 27 or x == 127:break
	#curses.flushinp()
	s.erase()

def GUI_help(env, screen):
	s = curses.newwin(20,78,3,1);
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	# Draw menu
	error, content = openfile('./help.txt')
	if error != "OK":content = error
	else:showSelection(s, env, content)

if __name__ == "__main__":
	print "Not a standalone program!"
