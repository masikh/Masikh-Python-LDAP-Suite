#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import curses,ldap,string
from os import system

def getInput(screen,offset_y,offset_x,length,alfabet,cursor):
        allowed = {     0 : (set("y" + "Y" + "n" + "N"),
                            "Use yY/nN only!"),
                        1 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+" + ":"),
                            "Use -_.+: a-z A-Z 0-9 only"),
                        2 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+" + "=" + "," + ":"),
                            "Use -_.+=,: a-z A-Z 0-9 only")
                  }
        wy,wx=screen.getmaxyx()
        i = 0
        value = ""
        while True:
                if cursor:curses.curs_set(1);curses.echo()
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
                elif length == 1:
			curses.curs_set(0)
			curses.noecho()
			value += string_x
			return value
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
	curses.noecho()
        return value

def login(LDAPSERVER,BASEDN,BINDDN,LDAPPW):
	if LDAPSERVER == "":return "Servername can't be empty!"
	if BASEDN == "":return "Base dn can't be empty!"
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	ldap.set_option(*options[0])	
	connection = ldap.initialize('%s'%LDAPSERVER)
	connection.set_option(ldap.OPT_NETWORK_TIMEOUT, 5.0)
	results = "Authentication at %s succesful" % (LDAPSERVER)

	if BINDDN == "":results = "Anonymous bind at %s succesful" % (LDAPSERVER)

	try:
		connection.simple_bind_s(BINDDN,LDAPPW)
	except ldap.INVALID_CREDENTIALS:
		results = "Credential failure."
	except ldap.INVALID_DN_SYNTAX:
		results = "Invalid DN syntax."
	except ldap.UNWILLING_TO_PERFORM:
		results = "Unwilling to perform."
	except ldap.SERVER_DOWN:
		results = "Cannot reach server"
	except ldap.LDAPError, e:
		results = e
	return results

def helper_login(env,screen):
	LDAPSERVER,BASEDN,BINDDN,LDAPPW=env.LDAPSERVER,env.BASEDN,env.BINDDN,env.LDAPPW
	s = screen.subwin(20, 78, 3, 1)
	s.keypad(1)
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.box()
	s.addstr(2, 2, "Login", curses.color_pair(3))
	s.refresh()
	try:LDAPPW
	except:LDAPPW=""

	reset=False
	if LDAPSERVER != "" and BASEDN != "":
		reset=True
		s.addstr(4, 2, "Connecting to %s"%LDAPSERVER,curses.color_pair(2))
		s.refresh()
		error = login(LDAPSERVER,BASEDN,BINDDN,LDAPPW)
		s.addstr(4, 2," " *75)
		s.addstr(19, 2, "[%s]"%error, curses.color_pair(1))
		if error == "Credential failure.":
			BINDDN = LDAPPW = ""
			reset=False
		if error == "Cannot reach server":
			reset=True
	if LDAPSERVER != "":s.addstr(4, 2,"Servername: %s"%(LDAPSERVER), curses.color_pair(2))
	else:
		s.addstr(4, 2,"Servername: ", curses.color_pair(1))
		LDAPSERVER = getInput(s,4,14,60,2,True)

	if BASEDN != "":s.addstr(5, 2,"Base DN:    %s"%(BASEDN), curses.color_pair(2))
	elif not reset:
		s.addstr(5, 2,"Base DN:    ", curses.color_pair(1))
		BASEDN = getInput(s,5,14,60,2,True)
	if BINDDN != "":s.addstr(6, 2,"Bind DN:    %s"%(BINDDN), curses.color_pair(2))
	elif not reset:
		s.addstr(19, 2,"[Leave empty for anonymous bind]", curses.color_pair(2))
		s.addstr(6, 2,"Bind DN:    ", curses.color_pair(1))
		BINDDN = getInput(s,6,14,60,2,True)
	if reset:
		s.addstr(8, 2, "reset values? [y,[n]]", curses.color_pair(1))
		result = getInput(s,8,24,1,0,False)
		if str(result) in ("y","Y"):
			env.LDAPSERVER = env.BASEDN = env.BINDDN = env.LDAPPW = ""
			s.erase()
			return env
	elif BINDDN != "":
		s.addstr(7, 2, "Password: ", curses.color_pair(1))
		curses.curs_set(0)
		curses.noecho()
		LDAPPW = s.getstr(7, 14, 60)
		error = login(LDAPSERVER,BASEDN,BINDDN,LDAPPW)
		s.addstr(9, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
		s.getch()
	else:
		s.addstr(8, 2, "Connecting to %s"%LDAPSERVER,curses.color_pair(2))
		s.refresh()
		error = login(LDAPSERVER,BASEDN,BINDDN,LDAPPW)
		s.addstr(8, 2, " "*75)
                s.addstr(8, 2, error, curses.color_pair(2))
                s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		
	env.LDAPSERVER,env.BASEDN,env.BINDDN,env.LDAPPW = LDAPSERVER,BASEDN,BINDDN,LDAPPW
	s.refresh()
	s.erase()
	return env
