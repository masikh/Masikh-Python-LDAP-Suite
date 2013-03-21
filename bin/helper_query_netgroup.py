#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 Robert Nagtegaal <masikh@gmail.com>
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import argparse,curses,ldap,ldif,re,scroller,string,sys
from os import system

def helper_query_netgroups(UID,env):
        DN="ou=netgroup," + env.BASEDN
        FILTER="(&(objectClass=nisNetgroup)(nisNetgroupTriple=*," + UID + ",*))"
        ATTR=[ "cn" ]
	try:
	        connection = ldap.open(env.LDAPSERVER)
	        connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_ONELEVEL, str(FILTER), ATTR)
	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	connection.unbind()
        if result == []:result = [("No such user!",{"": ""})]
	return (result)

def helper_query_allgroups(env):
        DN="ou=netgroup," + env.BASEDN
        FILTER="cn=*"
        ATTR=[ "cn" ]
	try:
	        connection = ldap.open(env.LDAPSERVER)
	        connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	connection.unbind()
	result.sort(key=lambda tup: tup[1])
        return (result)

def helper_query_dn(NETGROUP,env):
	DN="ou=netgroup," + env.BASEDN
	FILTER="cn=" + NETGROUP
	ATTR=[ "cn" ]
	try:
		connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	if result == []:result = [("No such netgroup!",{"": ""})]
	connection.unbind()
	return (result)	

def helper_query_membergroups(NETGROUP,env):
        DN="ou=netgroup," + env.BASEDN
        FILTER="cn=" + NETGROUP
        ATTR=[ "memberNisNetgroup" ]
	try:
	        connection = ldap.open(env.LDAPSERVER)
	        connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_ONELEVEL, FILTER, ATTR)
        except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	connection.unbind()
        return (result)

def helper_query_hosttriples(NETGROUP,env):
        DN="ou=netgroup," + env.BASEDN
        FILTER="(&(objectClass=nisNetgroup)(cn=" + NETGROUP + ")(nisNetgroupTriple=\(*,,*\)))"
        ATTR=None
	try:
	        connection = ldap.open(env.LDAPSERVER)
	        connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	connection.unbind()
        return (result)

def helper_query_usertriples(NETGROUP,env):
        DN="ou=netgroup," + env.BASEDN
        FILTER="(&(objectClass=nisNetgroup)(cn=" + NETGROUP + ")(nisNetgroupTriple=\(-,*,*\)))"
        ATTR=None
	try:
	        connection = ldap.open(env.LDAPSERVER)
	        connection.simple_bind_s()
       		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	connection.unbind()
        return (result)

def helper_query(NETGROUP,env):
        output = "Distinguished name of netgroup " + NETGROUP + "\n" 
	output += "-------------------------------------" + "\n"
        result = helper_query_dn(NETGROUP,env)
        for dn,entry in result:
		output +=  "dn: " + dn + "\n\n"               
	result = helper_query_membergroups(NETGROUP,env)
	output +=  "Member nis-groups of nis-group " + NETGROUP + "\n"
	output +=  "-------------------------------------" + "\n"
	for dn,entries in result:
		for memberNisNetgroup, member in dict.items(entries):	
			for multivalue in member:
				output +=  multivalue + "\n"
	result = helper_query_hosttriples(NETGROUP,env)	
	output +=  "\nHost triples in netgroup" + "\n"
	output +=  "-------------------------------------" + "\n"
	column = 0
	for dn,entries in result:
                for nisNetgroupTriple, host in dict.items(entries):   
                        if nisNetgroupTriple == "nisNetgroupTriple":
				for multivalue in host:
					if column > 2:
						column = 0
                                        	output += multivalue + "\n"
					else:
						column += 1
						output += multivalue + "\t"
	if column > 0:
		output += "\n"
	result = helper_query_usertriples(NETGROUP,env)
	output +=  "\nUser triples in netgroup" + "\n"
	output +=  "-------------------------------------" + "\n"
	for  dn,entries in result:
                for nisNetgroupTriple, host in dict.items(entries):   
                        if nisNetgroupTriple == "nisNetgroupTriple":
                                for multivalue in host:
					if column > 2:
						column = 0
                                        	output += multivalue + "\n"
					else:
						column += 1
						output += multivalue + "\t"
	return output

def helper_query_membership(UID,env):
        result = helper_query_netgroups(UID,env)
        print "Distinguished Name of " + UID + "'s netgroups"
        print "-------------------------------------"
        for dn,entry in result:
                print "dn: " + dn

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
                        screen.addstr(wy - 1, 2,"(Wrong input: %s)"%(allowed    [alfabet][1]),curses.color_pair(1))
                        screen.addstr(offset_y, offset_x, "%s"%(value))
                        continue
                elif length == 1:
                        curses.curs_set(0)
                        curses.noecho()
                        value += string_x
                        return value
                elif i >= length:
                        screen.addstr(wy - 1, 2,"(No more than %s characters     allowed)"%(length),curses.color_pair(1))
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

def query_group(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.erase()
        s.box()
        s.addstr(2, 2, "Query netgroup information", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter netgroup: ", curses.color_pair(1))
        NETGROUP = getInput(s,4,18,58,2,True)
	if NETGROUP == "":
		s.erase()
		return
        result = helper_query(NETGROUP,env)
        s.keypad(1)
        scroller.scroller(s, result,"Query netgroup information")
	s.erase()

def query_allgroups(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	s.erase()
        s.box()
        result = helper_query_allgroups(env)
	output = ""
	for dn,entry in result:
                output +=  "dn: " + dn + "\n"
	s.keypad(1)
        scroller.scroller(s, output, "Query all netgroups")
	s.erase()

def query_user_netgroup(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.erase()
        s.box()
        s.addstr(2, 2, "Query netgroup membership", curses.color_pair(3))
        s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
        UID = getInput(s,4,18,58,2,True)
        if UID == "":
		s.erase()
		return
        result = helper_query_netgroups(UID,env)
        output = ""
        for dn, entries in result:
                output += "dn: " + dn + "\n"
        s.keypad(1)
        scroller.scroller(s, output, "Query user's netgroup membership")
	s.erase()

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='This program shows netgroup information.')
        action = parser.add_mutually_exclusive_group(required=True)
        action.add_argument('-g', action='store', nargs=1, metavar='group', help='Show netgroup information')
        action.add_argument('-a', action='store_true', help='Show all netgroups')
        action.add_argument('-m', action='store', nargs=1, metavar='user', help='Show user netgroup membership')
        parser.set_defaults(g=['None'],m=['None'])
        args = vars(parser.parse_args())
        g = args['g'][0]
        a = args['a']
	m = args['m'][0]
        if g!='None':print helper_query(g)
        if a:	
		result=helper_query_allgroups(env)
		for dn,entry in result:
                        print "dn: " + dn
	if m!='None':helper_query_membership(m,env)
	exit(1)
