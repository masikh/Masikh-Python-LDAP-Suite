#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import curses,traceback,os,string
from os import system
os.putenv("ESCDELAY", "25") # no delay after pressing ESC key

import helper_query_autofs as query_autofs
#import helper_show_logs as query_logs
import helper_query_user as query_user
import helper_query_netgroup as query_netgroup
import helper_query_groups as query_groups
import helper_modify_netgroup as modify_netgroup
import helper_modify_group as modify_group
import helper_modify_user as modify_user
import helper_modify_transaction as modify_transaction
import helper_query_transaction as query_transactions
import helper_help as helper_help
import environment as environment
import login as login

def getInput(screen,offset_y,offset_x,length,alfabet):
	allowed = { 	0 : (set("y" + "Y" + "n" + "N"),
			    "Use yY/nN only!"),
			1 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+"),
			    "Use -_.+ a-z A-Z 0-9 only"),
			2 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+" + "=" + ","),
			    "Use -_.+=, a-z A-Z 0-9 only")
		  }
	wy,wx=screen.getmaxyx()
	i = 0
	value = ""
	while True:
		curses.curs_set(1)
		x = screen.getch()
		screen.hline(wy - 1, 2, curses.ACS_HLINE, 75)
		if x < 255:string_x = chr(x)
		else:string_x = str(x)
		
		if x == ord('\n'):break
		elif x == 27:value = "";break
		elif x == 127 or x == 263:
			value = value[:-1]
			if i > 0:i -= 1
			x = ""
			screen.addstr(offset_y, offset_x, " " * (length))
			screen.addstr(offset_y, offset_x, "%s"%(value))
			continue	
		elif string_x not in allowed[alfabet][0]:
			screen.addstr(wy - 1, 2,"(Wrong input: %s)"%(allowed[alfabet][1]),curses.color_pair(1))
			screen.addstr(offset_y, offset_x, "%s"%(value))
			continue	
		elif i >= length:
			screen.addstr(wy - 1, 2,"(No more than %s characters allowed)"%(length),curses.color_pair(1))
			screen.addstr(offset_y, offset_x, "%s"%(value))
			continue
		else:value += string_x
		screen.addstr(offset_y, offset_x, "%s"%(" "*length))
		screen.addstr(offset_y, offset_x, "%s"%(value))
		x = ""
		i += 1
	curses.curs_set(0)
	return value

def sub(menupath,screen):
	s = screen.subwin(20,78,3,1);
	s.erase()
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	# Draw menu
	s.box()
	s.addstr(16, 4, " "*65, curses.color_pair(0))
	s.addstr(16, 4, "Function: '%s' called."%menupath, curses.color_pair(0))
	s.addstr(17, 4, "Input: ", curses.color_pair(0))
	value = getInput(s, 17, 11, 8, 1)
	if value == "":
		s.erase()
		return
	s.addstr(18, 4, "Your input: %s"%(value), curses.color_pair(0))
	s.getch()
	s.erase()
	return # Just a subroutine 

def dummy(x,y):return # Called on exit!

def menus():
	menu_search_user = { "SFERP" : {"top" : False, 
					"vertical" : True,
					"text_offset_yx" : (0,2),
					"window_offset_yx" : (3,7) },
			   "0" 	     : (query_user.query_users,"By part of username","p",3),
			   "1" 	     : (query_user.query_user,"Information","I",0),
			   "2" 	     : (query_autofs.helper_query_autofs,"Autofs entries","A",0) }
	menu_search_group = { "SFERP" : {"top" : False,
					"vertical" : True,
					"text_offset_yx" : (0,2),
					"window_offset_yx" : (4,7) },
			   "0" 	     : (query_groups.query_groups_byall,"Show all groups","S",0),
			   "1" 	     : (query_groups.query_groups_byuser,"By user name","u",3),
			   "2" 	     : (query_groups.query_groups_bygroup,"By group name","g",3) }
	menu_search_netgroup = { "SFERP" : {"top" : False,
					"vertical" : True,
					"text_offset_yx" : (0,2),
					"window_offset_yx" : (5,7) },
			   "0" 	     : (query_netgroup.query_allgroups,"Show all netgroups","n",9),
			   "1" 	     : (query_netgroup.query_user_netgroup,"Show Membership","m",5),
			   "2" 	     : (query_netgroup.query_group,"Information","I",0) }
	menu_search    = { "SFERP"   : {"top" : False,
					"vertical" : True,
					"text_offset_yx" : (0,2),
					"window_offset_yx" : (2,3) },
			   "0"       : (menu_search_user,"User","U",0),
			   "1"       : (menu_search_group,"Group","G",0),
               		   "2"       : (menu_search_netgroup,"Netgroup","N",0),
               		   "3"       : (query_transactions.GUI_show_transactions,"Transactions ","T",0) }
	menu_modify_user      = { "SFERP"   : {	"top" : False,
						"vertical" : True,
						"text_offset_yx" : (0,2),
						"window_offset_yx" : (3,25) },
			   "0"       : (modify_user.GUI_add_user,"Add user","A",0),
			   "1"       : (modify_user.GUI_del_user,"Delete user","D",0),
			   "2"       : (modify_user.GUI_change_password,"Change user password","C",0),
               		   "3"       : (modify_user.GUI_modify_user,"Modify user attributes","M",0),
			   "4"       : (modify_user.GUI_multiple_add_user,"Add multiple users","u",5) }
	menu_modify_group     = { "SFERP"   : {"top" : False,
					       "vertical" : True,
					       "text_offset_yx" : (0,2),
					       "window_offset_yx" : (4,25) },
			   "0"       : (modify_group.GUI_add_group,"Add new group","A",0),
			   "1"       : (modify_group.GUI_del_group,"Delete group","D",0),
			   "2"       : (modify_group.GUI_modify_group,"Modify group","M",0),
			   "3"       : (modify_group.GUI_add_user,"Link user to group","L",0),
                	   "4"       : (modify_group.GUI_del_user,"Unlink user from group","U",0) }
	menu_modify_netgroup_link  = { "SFERP"   : {"top" : False,
					       "vertical" : True,
					       "text_offset_yx" : (0,2),
					       "window_offset_yx" : (8, 29) },
			   "0"       : (modify_netgroup.add_user_to_netgroup,"User to netgroup","U",0),
			   "1"       : (modify_netgroup.add_host_to_netgroup,"Host to netgroup","H",0),
                	   "2"       : (modify_netgroup.add_netgroup_to_netgroup,"Netgroup to netgroup","N",0) }
	menu_modify_netgroup_unlink  = { "SFERP"   : {"top" : False,
					       "vertical" : True,
					       "text_offset_yx" : (0,2),
					       "window_offset_yx" : (9,29) },
			   "0"       : (modify_netgroup.del_user_from_netgroup,"User from netgroup","U",0),
			   "1"       : (modify_netgroup.del_host_from_netgroup,"Host from netgroup","H",0),
                	   "2"       : (modify_netgroup.del_netgroup_from_netgroup,"Netgroup from netgroup","N",0) }
	menu_modify_netgroup  = { "SFERP"   : {"top" : False,
					       "vertical" : True,
					       "text_offset_yx" : (0,2),
					       "window_offset_yx" : (5,25) },
			   "0"       : (modify_netgroup.create_netgroup,"Add new netgroup","A",0),
			   "1"       : (modify_netgroup.delete_netgroup,"Delete netgroup","D",0),
			   "2"       : (menu_modify_netgroup_link,"Link entity to netgroup","L",0),
                	   "3"       : (menu_modify_netgroup_unlink,"Unlink entity from netgroup ","U",0) }
	menu_modify    = { "SFERP"   : {"top" : False,
					"vertical" : True,
					"text_offset_yx" : (0,2),
					"window_offset_yx" : (2,21) },
			   "0"       : (menu_modify_user,"User","U",0),
			   "1"       : (menu_modify_group,"Group","G",0),
			   "2"       : (menu_modify_netgroup,"Netgroup","N",0),
                	   "3"       : (modify_transaction.GUI_modify_transaction,"Transaction","T",0) }
	menu_top       = { "SFERP"   : {"top" : True,
					"vertical" : False,
					"text_offset_yx" : (1,5),
					"window_offset_yx" : (1,0)},
			   "0"       : (menu_search,"Search","S",0),
               		   "1"       : (menu_modify,"Modify","M",0),
			   "2"       : (login.helper_login,"Login","L",0),
			   "3"       : (helper_help.GUI_help,"Help","H",0),
			   "4"	     : (dummy,"Exit","x",1) }
	return menu_top

def getspacing(menu):
	topmenu = menu['SFERP']['top']
	stringlength = numitems = i = 0
	offset_x = menu['SFERP']['window_offset_yx'][1]
	for item in menu:
		if item == "SFERP":continue
		else:
			stringlength += len(menu[str(i)][1])
			numitems += 1
			#i += 1
	if numitems < 1:numitems = 1
	elif numitems > 2:numitems -= 1
	spacing = int((76.0 - offset_x - float(stringlength)) / (float(numitems)))
	if not topmenu:spacing = 2 
	return spacing

def drawmenu(menu,pos,screen):
	# SFERP == PREFS (prefs might be used as menu item!)
	vertical = menu['SFERP']['vertical']
	offset_x = menu['SFERP']['text_offset_yx'][1]
	offset_y = menu['SFERP']['text_offset_yx'][0]
	spacing = getspacing(menu)
	selection = breadcrumb = next_location = ""
	
	# Draw fancy box()
	screen.box()

	# get longest string in menu:
	menu_item = longest = 0
	for item in menu:
		# Omit the preferences as menu item!
		if item == "SFERP":continue
		else:
			if longest < len(menu[item][1]):
				longest = len(menu[item][1])

	i = 1
	for item in menu:
		# Omit the preferences as menu item!
		if item == "SFERP":continue
		if type(menu[item][0]) == dict:submenu = True
		else:submenu = False
		# draw current menu vertical
		if vertical:
			if pos == i:
				extra = longest - len(menu[str(menu_item)][1]) + 1
				if submenu:
					screen.addstr(i, offset_x - 1," " + menu[str(menu_item)][1] + " " * (extra - 1) + ">", curses.color_pair(3))
				else:
					screen.addstr(i, offset_x - 1," " + menu[str(menu_item)][1] + " " * extra, curses.color_pair(3))
				screen.addstr(i, offset_x + menu[str(menu_item)][3],menu[str(menu_item)][2], curses.color_pair(3))
				selection = menu[str(menu_item)][0]
				next_location = str(menu_item)
				breadcrumb = menu[str(menu_item)][1]
			else:
				extra = longest - len(menu[str(menu_item)][1]) + 1
				if submenu:
					screen.addstr(i, offset_x - 1, " " + menu[str(menu_item)][1] + " " * (extra - 1) + ">", curses.color_pair(2))
				else:
					screen.addstr(i, offset_x - 1, " " + menu[str(menu_item)][1] + " " * extra, curses.color_pair(2))
				screen.addstr(i, offset_x + menu[str(menu_item)][3],menu[str(menu_item)][2], curses.color_pair(1))
			i+=1
			menu_item += 1
		# Draw current menu horizontal
		else:
			# If current item is selected
			if pos == i:
				if i == 1:
					screen.addstr(offset_y, offset_x,menu[str(menu_item)][1], curses.color_pair(3))
				else:
					screen.addstr(offset_y, offset_x,menu[str(menu_item)][1], curses.color_pair(3))
				screen.addstr(offset_y, offset_x + menu[str(menu_item)][3],menu[str(menu_item)][2], curses.color_pair(3))
				selection = menu[str(menu_item)][0]
				next_location = str(menu_item)
				breadcrumb = menu[str(menu_item)][1]
			else:
				if i == 1:
					screen.addstr(offset_y, offset_x, menu[str(menu_item)][1], curses.color_pair(2))
				else:
					screen.addstr(offset_y, offset_x, menu[str(menu_item)][1], curses.color_pair(2))
				screen.addstr(offset_y, offset_x + menu[str(menu_item)][3],menu[str(menu_item)][2], curses.color_pair(1))
			offset_x += len(menu[str(menu_item)][1]) + spacing
			i+=1
			menu_item += 1
	return breadcrumb,next_location

def getwindowsize_vertical(menu):
	x = y = 0
	for item in menu:
		if item == "SFERP":continue
		else:
			length=len(menu[item][1])
			if length > x:x=length
			y += 1
	return y,x+2

def getwindowsize_horizontal(menu):
	x = i = 0
	for item in menu:
		if item == "SFERP":continue
		else:
			x += len(menu[item][1])
			i += 1
	x += i	
	return 1, x + 2

def winRefresh(winlist):
	for window in winlist:
		window.refresh()
	return

def SetupColors():
	# Setup colors
	curses.curs_set(0)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	return

def SetupMenuWindow(winlist,menu):
	# Setup window
	topmenu = menu['SFERP']['top']
	vertical = menu['SFERP']['vertical']
        offset_x = menu['SFERP']['window_offset_yx'][1]
        offset_y = menu['SFERP']['window_offset_yx'][0]
	if vertical:
		size_y,size_x = getwindowsize_vertical(menu)
	else:
		size_y,size_x = getwindowsize_horizontal(menu)
	if topmenu:
		s = winlist[0].subwin(24,80,0,0);s.hline(2, 1, curses.ACS_HLINE, 78)
	else:
		s = winlist[0].subwin(size_y+2,size_x+2,offset_y,offset_x)
	return s

def RedrawParentMenus(winlist,location):
	# Redraw all menu's
	temp = len(location); current = menus()
	for item in location:
		try:
			if current['SFERP']['vertical']:
				size_y,size_x = getwindowsize_vertical(current)
			else:
				size_y,size_x = getwindowsize_horizontal(current)
			if current['SFERP']['top']:
				window = winlist[0].subwin(24,80,0,0)
			else:
				window = winlist[temp].subwin(size_y+2,size_x+2,current['SFERP']['window_offset_yx'][0],current['SFERP']['window_offset_yx'][1])
			window.box()
			drawmenu(current, int(location[temp]) + 1,window)
			current = current[location[temp]][0]
			temp -= 1
		except:
			continue
	return

def DrawBreadCrumbs(winlist, bread, breadcrumb):
	winlist[0].hline(23, 1, curses.ACS_HLINE, 78)
	if bread == "":
		winlist[0].addstr(23,3,"[%s]"%(breadcrumb),curses.color_pair(2))
	else:
		breadcrumbs = "%s > %s"%(bread,breadcrumb)
		if len(breadcrumbs) > 72:
			breadcrumbs = breadcrumbs[-69:]
			winlist[0].addstr(23,3,"[...%s]"%(breadcrumbs),curses.color_pair(2))
		else: 
			winlist[0].addstr(23,3,"[%s]"%(breadcrumbs),curses.color_pair(2))
	return

def ParseHotKeys(x, menu, pos):
	i = 0 
	selection = None
	for item in menu:
		# Skip prefs item in menu
		if item == "SFERP":continue
		# If pressed hotkey is in current iteration of menu items do
		elif x == ord(str(menu[str(i)][2]).lower()) or x == ord(str(menu[str(i)][2]).upper()):
			pos = i + 1
			x = ""
		i += 1
	execute = True
	return pos, execute, x

def IfEnterPressed(x):
	execute = False
	if x == ord('\n'):
		execute = True
		x = ""
	return execute, x

def IfEscapePressed(x, menu):
	topmenu = menu['SFERP']['top']
	escape = False
	if menu['SFERP']['top']:
		return escape, x
	if x == 27 or x == 127 or x == 263:
		escape = True
		x = ""
	return escape, x

def is_function(f):
	return str(type(f)) == "<type 'function'>"

def IfArrowPressed(x, menu, pos):
	vertical = menu['SFERP']['vertical']
	topmenu = menu['SFERP']['top']
	escape = execute = False
	# Navigate through menu or execute function if right arrow key is pressed 
	if vertical:
		# down arrow goes down untill end of the list 
        	if x == 258:
        		if pos < len(menu) - 1:
				pos += 1
			x = ""
        	# up arrow quits menu if top of list is reached
        	elif x == 259:
        		if pos > 1:
				pos -= 1
			else:
				escape = True
			x = ""
				
		# left arrow leaves menu item
		elif x == 260:
			escape = True
			x = ""
		# right arrow opens menu item
		elif x == 261:
			execute = True
			x = ""
	else:
		# down arrow opens menu item
		if x == 258:
			execute = True
			x = ""
		# up arrow in submenu
		elif x == 259 and not topmenu:
			escape = True
			x = ""
		# left arrow
		elif x == 260:
			pos -= 1
			if pos == 0:pos = len(menu) - 1
			x = ""
		# right arrow
		elif x == 261:
			if pos == len(menu) - 1:pos = 1
                        else:pos += 1
			x = ""
	return execute, escape, pos, x

def currentmenu(menu, winlist, bread, location, env):
	pos = 1  
	escape = quit = False
	topmenu = menu['SFERP']['top']
	vertical = menu['SFERP']['vertical']
        offset_x = menu['SFERP']['window_offset_yx'][1]
        offset_y = menu['SFERP']['window_offset_yx'][0]

	# Setup window
	screen = SetupMenuWindow(winlist,menu)	

	# Append current menu window to list of windows.
	winlist += [screen]

	# Setup colors
	SetupColors()
	x = " "
	execute = False
	while not escape:
		screen.erase()
		# Redraw all parent menu's
		RedrawParentMenus(winlist, location)
		# Repair the topmenu line if we're the topmenu
		if topmenu:winlist[0].hline(2, 1, curses.ACS_HLINE, 79)
		# Draw current menu
		breadcrumb, next_location = drawmenu(menu,pos,screen)
		# Draw breadcrumbs
		DrawBreadCrumbs(winlist, bread, breadcrumb)
		
		# Refresh all windows
		winRefresh(winlist)	
	
		# get keyboard input
		x = winlist[0].getch()
		# Get new position in menu and selection when a hotkey is pressed.
		if x != "":pos, execute, x = ParseHotKeys(x, menu, pos)
		# Check if enter is pressed
		if x != "":execute, x = IfEnterPressed(x)
		# Check if arrow keys are pressed
		if x != "":execute, escape, pos, x = IfArrowPressed(x, menu, pos)
		# Check if esc/backscape is pressed (unless we're the top menu!)
		if x != "":escape,x = IfEscapePressed(x, menu)
		if x != "":x = ""
		selection = menu[str(pos - 1)][0]
		
		screen.erase()
		# Redraw all parent menu's
		RedrawParentMenus(winlist, location)
		# Repair the topmenu line if we're the topmenu
		if topmenu:winlist[0].hline(2, 1, curses.ACS_HLINE, 79)
		# Draw current menu
		breadcrumb, next_location = drawmenu(menu,pos,screen)
		# Draw breadcrumbs
		DrawBreadCrumbs(winlist, bread, breadcrumb)
		
		# Refresh all windows
		winRefresh(winlist)	
		
		# if selected item is dictionary a sub menu exists
		if type(selection) is dict and execute:
			location += next_location
			if bread == "": 
				currentmenu(selection, winlist, "%s"%(breadcrumb), next_location, env)
			else:
				currentmenu(selection, winlist, "%s > %s"%(bread, breadcrumb), location, env)
			location = location[:-1]
			winlist = winlist[:-1]
			execute = False
		elif is_function(selection) and execute:
			# STOP THE PROGRAM
			if menu[str(pos - 1)][1] == "Exit":
				escape = True
			# OR RUN MODULE
			selection(env,winlist[0])
			execute = False
	screen.erase()
	winRefresh(winlist)
	#winlist = winlist[:-1]
	#location = location[:-1]
	return

if __name__ == '__main__':
	winlist = list()
	env = environment.environment()
        try:
		# Initialize curses
		stdscr = curses.initscr()
		curses.noecho(); curses.cbreak()
		stdscr.keypad(1)		
	
		menu = menus()	
		winlist += [stdscr]
		location = []
		# Enter the main loop
		currentmenu(menu,winlist,"",location,env)
	
		# Set everything back to normal
		stdscr.keypad(0)
		curses.echo() ; curses.nocbreak()
		curses.endwin() 
	except:
		# In the event of an error, restore the terminal
		stdscr.keypad(0)
		curses.echo() ; curses.nocbreak()
		curses.endwin()
		traceback.print_exc()		# Print the exception
