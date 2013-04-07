#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import argparse,curses,getpass,ldap,ldif,re,scroller,string,sys
from os import system

class environment:
	LDAPSERVER=BASEDN=BINDDN=LDAPPW=""

def helper_query_user(UID,env):
        DN="%s,%s"%(env.PEOPLE,env.BASEDN)
        FILTER="(uid=" + UID + ")"
        ATTR=[	"sn",
		"loginShell", 
		"employeeType",
		"employeeNumber",
		"uidnumber",
		"gidnumber",
		"uid",
		"gecos",
		"cn",
		"homeDirectory",
		"objectClass"
	     ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
       	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
	if result == []:result = [("No such user!",{"": ""})]
	connection.unbind()
	return result 

def query_bypart(UID,env):
        DN="%s,%s"%(env.PEOPLE,env.BASEDN)
        FILTER="(&(objectClass=posixAccount)(uid=*" + UID + "*))"
        ATTR=["dn", "uid"]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
       	except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)","")] 
	connection.unbind_s()
	return result

def helper_query(UID,env):
        result = helper_query_user(UID,env)
        print "Contents of " + UID + "'s user contrainer"
	print "-------------------------------------"
	ldif_writer = ldif.LDIFWriter(sys.stdout)
        for dn,entry in result:
                ldif_writer.unparse(dn,entry)

def helper_query_users(UID,env):
        result = query_bypart(UID,env)
        if str(result) == "{'desc': 'Size limit exceeded'}":
                print "error code: Size limit exceeded\nTo many usernames returned, try more letters."
                return
        result.sort()
        ldif_writer = ldif.LDIFWriter(sys.stdout)
        temp=""
        for dn,entry in result:
                temp += "dn: " + dn + "\n"
        print temp
        return

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


def query_user(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	s.erase()
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Query user Information", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
	UID = getInput(s,4,18,58,2,True)
	if UID == "":
		s.erase()
		return
	result = helper_query_user(UID,env)
	output = ""
	for dn, entries in result:
		output += "dn: " + dn + "\n"
		for entry,value in dict.items(entries):
			for multivalue in value:
				output += entry + ": " + multivalue + "\n"
	s.keypad(1)
	scroller.scroller(s, output,"Query user Information")
	s.erase()

def query_users(env, screen):
        s = curses.newwin(20, 78, 3, 1)
        s.erase()
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	s.box()
	s.addstr(2, 2, "Query by (part of) username", curses.color_pair(3))
        s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
        UID = getInput(s,4,18,58,2,True)
        if UID == "":
		s.erase()
		return
        result = query_bypart(UID,env)
        if str(result) == "{'desc': 'Size limit exceeded'}":
                s.clear()
                scroller.scroller(s,"Size limit exceeded\nTo many usernames returned, try more letters.","ERROR:")
                return
        result.sort()
        ldif_writer = ldif.LDIFWriter(sys.stdout)
        temp=""
        for dn,entry in result:
                temp += "dn: " + dn + "\n"
        s.keypad(1)
        scroller.scroller(s,temp,"Query by (part of) username")
	s.erase()
	return
		
if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='This program queries user information.')
        parser.add_argument('uid', action='store', nargs=1, metavar='uid', help='username.')
	parser.add_argument('--host', action='store', nargs=1, metavar='ldapserver', help='ldap server. (required)', required=True)
	parser.add_argument('--basedn', action='store', nargs=1, metavar='basedn', help='basedn. (required)', required=True)
        parser.add_argument('-p', action='store_true', default=False, help='Search by part of username')
	parser.add_argument('--binddn', action='store', nargs=1, metavar='binddn', help='binddn.')
        parser.add_argument('-W', action='store_true', default=False, dest='passwordprompt', help='prompt for bind password')
        args = vars(parser.parse_args())
	#
	# must get basedn, servername (mand.) may get binddn, ldappw (opt.)
	#
	env = environment()
	env.LDAPSERVER=args['host'][0]
	env.BASEDN=args['basedn'][0]
	if args['passwordprompt']:
		try:env.BINDDN=args['binddn'][0]
		except:print "Password prompt without a binddn makes no sense.";exit(0)
		print env.BASEDN 
		env.LDAPPW = getpass.getpass()
	if args['p']:
		helper_query_users(args['uid'][0],env)
	else:
	        helper_query(args['uid'][0],env)
