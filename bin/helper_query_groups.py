#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 Robert Nagtegaal <masikh@gmail.com>
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

from os import system
import argparse,curses,ldap,string,sys
import scroller

def helper_query_groups_byuser(UID,env):
	output = warning = gidNumber = ""
        DN="ou=People," + env.BASEDN
        FILTER="(&(objectClass=PosixAccount)(uid=%s))"%(UID)
	ATTR = [ "gidNumber" ]
	try:
	        connection = ldap.open(env.LDAPSERVER)
	        connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	try:
	     gidNumber=result[0][1]["gidNumber"][0]
	except IndexError:
		gidNumber = "-1"
	except KeyError:
		gidNumber = "-1"
	DN="ou=Group,%s"%(env.BASEDN)
	FILTER="(&(objectClass=posixGroup)(gidNumber=%s))"%(gidNumber)
	ATTR = ["cn"]
	try:
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:
		result = [("Generic error occured (are you logged in?)",{"": ""})]
	if result == []:
		warning  = "\nWarning:\n\n\tPrimary group for user %s does not exist.\n"%(UID)
		warning += "\t%s's primairy gid is: %s\n"%(UID,gidNumber)
		warning += "\tYou'd might like to add a group with gidNumber: %s\n\n"%(gidNumber)
	output += "gidNumber Primairy group DN for user %s\n"%(UID)
	output += "--------- -------------------------------------\n"
	if warning != "":
		output += warning
	else:
		for dn,entry in result:
			output += "%s\t  dn: %s\n"%(gidNumber,dn)
        DN="ou=Group," + env.BASEDN
	FILTER="(&(objectClass=posixGroup)(memberUid=" + UID + "))"
	ATTR = None
        try:
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:
		result = [("Generic error occured (are you logged in?)",{"": ""})]
	connection.unbind()
	output += "\ngidNumber Non-primary groups DNs for user " + UID + "\n"
        output += "--------- -------------------------------------\n"
	if result != [('Generic error occured (are you logged in?)', {'': ''})]:
		for dn,entry in result:
			output += "%s\t  dn: %s\n"%(entry["gidNumber"][0], dn)
	return output

def helper_query_groups_bygroup(GROUP,env):
        output = ""
        DN="ou=Group," + env.BASEDN
        FILTER="(&(objectClass=posixGroup)(cn=" + GROUP + "))"
        ATTR1 = [ "memberUid" ]
        ATTR2 = [ "gidNumber" ]
	try:
		connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
        	result1 = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR1)
		result2 = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR2)
	except ldap.LDAPError, e:
		output += "Generic error occured (are you logged in?)\n"
		return output
	if result1 == []:result1 = [("",{"memberUid": ["No such group!"]})]
	GROUPID = result2[0][1]['gidNumber'][0]
	output += "Members of group %s (gidNumber: %s)\n"%(GROUP,GROUPID)
        output += "-------------------------------------\n"
	for dn,entry in result1:
		for memberUid in entry:
			for member in entry[memberUid]:
				output += "memberUid: " + member + "\n"
	return output

def helper_query_groups_all(env):
        output = ""
        DN="ou=Group," + env.BASEDN
        FILTER="(&(objectClass=posixGroup)(cn=*))"
        ATTR = [ "cn" ]
	try:
	        connection = ldap.open(env.LDAPSERVER)
	        connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	result.sort(key=lambda tup: tup[1])
	for dn,entry in result:
		output += "dn: " + dn + "\n"
	return output

def getInput(screen,offset_y,offset_x,length,alfabet,cursor):
	allowed = {     0 : (set("y" + "Y" + "n" + "N"),
                           "Use yY/nN only!"),
                       1 : (set(string.digits + string.ascii_letters + "-"     + "_" + "." + "+"),
                           "Use -_.+ a-z A-Z 0-9 only"),
                        2 : (set(string.digits + string.ascii_letters + "-"     + "_" + "." + "+" + "=" + ","),
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


def query_groups_byuser(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.erase()
        s.box()
        s.addstr(2, 2, "Query groups by user", curses.color_pair(3))
        s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
        UID = getInput(s,4,18,58,2,True)
	if UID == "":
		s.erase()
		return
        result = helper_query_groups_byuser(UID,env)
        scroller.scroller(s, result,"Query groups by user")
	s.erase()

def query_groups_bygroup(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.erase()
        s.box()
        s.addstr(2, 2, "Query group by name", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter groupname: ", curses.color_pair(1))
        GROUP = getInput(s,4,19,57,2,True)
	if GROUP == "":
		s.erase()
		return
        result = helper_query_groups_bygroup(GROUP,env)
        scroller.scroller(s, result,"Query group by name")
	s.erase()

def query_groups_byall(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	s.erase()
        s.box()
        result = helper_query_groups_all(env)
        scroller.scroller(s, result,"Query all groups")
	s.erase()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This program shows group information for users and groups.')
	action = parser.add_mutually_exclusive_group(required=True)
	action.add_argument('-u', action='store', nargs=1, metavar='user', help='Show users group membership')
	action.add_argument('-g', action='store', nargs=1, metavar='group', help='Show group information')
	action.add_argument('-a', action='store_true', help='Show all user groups')
	parser.set_defaults(u=['None'], g=['None'])
	args = vars(parser.parse_args())
	u = args['u'][0]
	g = args['g'][0]
	a = args['a']
	if u!='None':print helper_query_groups_byuser(u)
	if g!='None':print helper_query_groups_bygroup(g)
	if a:print helper_query_groups_all()
