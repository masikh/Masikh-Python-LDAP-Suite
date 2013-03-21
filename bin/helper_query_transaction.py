#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 Robert Nagtegaal <masikh@gmail.com>
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import curses,os,re,time
import helper_apply_ldif as apply_ldif

def getUndofiles(env):
	# Get logfiles as list and omit dotfiles
	dirList = [f for f in os.listdir(env.LOGS) if f.endswith('.ldif')]
        
        # Initialize dictonairies for logfiles
        logfiles = []
       	revertables = []

	# If no logfiles found skip else
	if dirList == []:
		indexed_logs = { 0 : {'tid' : 0, 'type' : 'NO LOGS FOUND!', 'action' : 'None', 'entity' : 'None', 'filename' : 'None' }}
		return indexed_logs 
	else:
	        # Build a dictionary of all log files
	        for file in dirList:
	                # Make an array of filename part with field seperator "."
	                t = file.split(".")
	                # Build a tuple and append it to the logfiles dictionary
			x = {	'tid': str(t[0]),
				'type' : t[1],
				'action': t[2],
	                 	'entity': t[3],
	                 	'filename': file
			    }
	                logfiles.append(x)

	# Get all undoable transactions  
        count = 0
	for row in logfiles:
		revertables.append(logfiles[count])
		count += 1       
        
	# Sort the list by tid in reverse order
	revertables.sort(key=lambda tup: tup["tid"], reverse=True)

	# Make a dict like { 0: {}, 1: {} ...}
	indexed_logs = dict(enumerate(revertables))
	
	# return the indexed_logs	
	return indexed_logs

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

def showSelection(s, env, selection):
	selection = "%s%s"%(env.LOGS,selection)
	error, content = openfile(selection)
	if error != "OK":return error
	length = width = 0 
	temp = content
	for i in temp.split('\n'):
		length +=1
		if len(i) > width:width = len(i)
	
	if length < 1 or width < 1:
		s.erase()
		s.box()
		s.addstr(2, 2, "Undo transaction", curses.color_pair(3))
		s.addstr(5,4,"Error: Empty file!",curses.color_pair(2))
		s.addstr(19,2,"[Press any key to continue]",curses.color_pair(1))
		s.getch()
		s.erase()
		return
	else:length += 1
	width += 9 
	mypad = curses.newpad(length, width)
	mypad_posx = mypad_posy = 0
	s.erase()
	s.box()
	s.hline(19, 2, curses.ACS_HLINE, 70)
	s.addstr(19,2,"[Use [ESC] to abort and [ARROWS] to scroll]",curses.color_pair(1))
	s.refresh()
	while True:
		mypad.refresh(mypad_posy, mypad_posx, 4, 3, 21, 76)
		i = 1 
		for line in content.split('\n'):
			mypad.addstr(i, 2, "%s"%(line), curses.color_pair(2))
			i += 1
			mypad.refresh(mypad_posy, mypad_posx, 4, 3, 21, 76)
		x = s.getch()
		# Down arrow (scroll down in text)
		if x == 258:
			if mypad_posy < length - 19:mypad_posy += 1
			mypad.refresh(mypad_posy, mypad_posx, 4, 3, 21, 76)
		# Up arror (scroll up in text)
		if x == 259 and mypad_posy > 0:
			mypad_posy -= 1
			mypad.refresh(mypad_posy, mypad_posx, 4, 3, 21, 76)
		if  x == 260 and mypad_posx > 0:
			mypad_posx -= 1
			mypad.refresh(mypad_posy, mypad_posx, 4, 3, 21, 76)
		if x == 261 and mypad_posx < width - 80:
			mypad_posx += 1
			mypad.refresh(mypad_posy,mypad_posx, 4, 3, 21, 76)
		if x == 27 or x == 127:break
	#curses.flushinp()
	s.erase()

def selectEntry(s, env, logfiles, pos = 0):
	curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	length = len(logfiles)
	mypad = curses.newpad(length + 9,76)
	if pos < 5:pad_pos = 0
	else:pad_pos = pos - 5 
	selection = None 
	s.addstr(19,2,"[Usage: [ESC] abort [ENTER] Show transaction]",curses.color_pair(1))
	s.addstr(4, 2,"Transaction",curses.color_pair(2))
	s.addstr(4,15,"Entity",curses.color_pair(2))
	s.addstr(4,24,"Date",curses.color_pair(2))
	s.addstr(4,50,"Type",curses.color_pair(2))
	s.addstr(4,69,"Action",curses.color_pair(2))
	s.hline(5, 2, curses.ACS_HLINE, 74)
	while True:
		s.refresh()
		for log in logfiles:
			date = time.ctime(float(logfiles[log]['tid']))
			if pos == log:
				mypad.addstr(log, 0, "%s"%(logfiles[log]['tid']), curses.color_pair(1))
				mypad.addstr(log, 13, "%s"%(logfiles[log]['entity']), curses.color_pair(1))
				mypad.addstr(log, 22, "%s"%(date), curses.color_pair(1))
				mypad.addstr(log, 48, "%s"%(logfiles[log]['type']), curses.color_pair(1))
				mypad.addstr(log, 67, "%s"%(logfiles[log]['action']), curses.color_pair(1))
			else:
				mypad.addstr(log, 0, "%s"%(logfiles[log]['tid']), curses.color_pair(2))
				mypad.addstr(log, 13, "%s"%(logfiles[log]['entity']), curses.color_pair(2))
				mypad.addstr(log, 22, "%s"%(date), curses.color_pair(2))
				mypad.addstr(log, 48, "%s"%(logfiles[log]['type']), curses.color_pair(2))
				mypad.addstr(log, 67, "%s"%(logfiles[log]['action']), curses.color_pair(2))
		mypad.refresh(pad_pos, 0, 9, 3, 20, 76)
		x = s.getch()		
		if x == 27 or x == 127:
			selection = None
			break
		if x == 258 and pos < len(logfiles) - 1:pos += 1
		if x == 259 and pos > 0:pos -= 1
		if x == ord('\n') and length > 0:
			selection = str(logfiles[pos]['filename'])
			error = showSelection(s, env, selection)
			s.erase()
			s.box()	
	        	s.addstr(2, 2, "Show transaction", curses.color_pair(3))
			s.addstr(19,2,"[Usage: [ESC] abort [ENTER] Show transaction]",curses.color_pair(1))
			s.addstr(4, 2,"Transaction",curses.color_pair(2))
			s.addstr(4,15,"Entity",curses.color_pair(2))
			s.addstr(4,24,"Date",curses.color_pair(2))
			s.addstr(4,50,"Type",curses.color_pair(2))
			s.addstr(4,69,"Action",curses.color_pair(2))
			s.hline(5, 2, curses.ACS_HLINE, 74)
		if pos - pad_pos > 11:pad_pos += 3
		if pos - pad_pos < 0:pad_pos -= 3
	return selection, pos

def GUI_show_transactions(env, screen):
	s = curses.newwin(20,78,3,1)
	s.keypad(1)
	curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
       	pos = 0
	while True:
		stop = False
		s.erase()
		s.box()
	        s.addstr(2, 2, "Show transaction", curses.color_pair(3))
		logfiles = getUndofiles(env)
		selection, pos = selectEntry(s, env, logfiles, pos)
		if selection == None:
			s.erase()
			break	

if __name__ == "__main__":
	print "Not a standalone program!"
