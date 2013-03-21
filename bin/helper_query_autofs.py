#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 Robert Nagtegaal <masikh@gmail.com>
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import argparse,curses,ldap,ldif,re,string,sys
from os import system

def helper_query_homedir(UID,env):
	DN="ou=auto.home,ou=Autofs," + env.BASEDN
	FILTER="(&(objectClass=automount)(cn=" + UID + "))"
	ATTR=["automountInformation"]
	try:
		connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"automountInformation": [""]})]
	if result == []:result = [("No such user!",{'automountInformation': [""]})]
	connection.unbind()
	return (result)

def helper_query_direct(env):
	DN="ou=auto.direct,ou=Autofs," + env.BASEDN
	FILTER="(&(objectClass=automount)(cn=*))"
	ATTR=["automountInformation"]
	try:
		connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"automountInformation": [""]})]
	connection.unbind()
	return (result)

def helper_query(UID,env):
	result = helper_query_homedir(UID,env)
	result += helper_query_direct(env)
	ldif_writer = ldif.LDIFWriter(sys.stdout)
	for dn,entry in result:
		ldif_writer.unparse(dn,entry)

def getInput(screen,offset_y,offset_x,length,alfabet,cursor):
	allowed = {     0 : (set("y" + "Y" + "n" + "N"),
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
                        screen.addstr(wy - 1, 2,"(No more than %s characters allowed)"%(length),curses.color_pair(    1))
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

def helper_query_autofs(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	s.erase()
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Query Autofs", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
        UID = getInput(s,4,18,60,1,True)
	if UID == "":
		s.erase()
		return
	result = helper_query_homedir(UID,env)
        result += helper_query_direct(env)
        ldif_writer = ldif.LDIFWriter(sys.stdout)
	count = 6
	for dn,entry in result:
		s.addstr(count, 2, "dn: " + dn,curses.color_pair(2))	
		s.addstr(count+1, 2, entry['automountInformation'][0],curses.color_pair(2))
		count += 3
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.refresh()
	s.getch()
	s.erase()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This program queries a users autofs entries in LDAP.')
	parser.add_argument('uid', action='store', nargs=1, metavar='uid', help='LDIF file.')
	args = vars(parser.parse_args())
	uid = args['uid'][0]
	helper_query(uid, env)
