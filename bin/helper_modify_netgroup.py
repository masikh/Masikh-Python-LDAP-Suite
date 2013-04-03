#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import argparse,curses,getpass,ldap,ldif,re,scroller,string,sys,time
import helper_apply_ldif as apply_ldif
from os import system

class environment:
        LDAPSERVER=BASEDN=BINDDN=LDAPPW=""
        LDBUG = False
        VERBOSE = False

def WriteLog(content,fname, env):
	timestamp = int(time.time())
	fname = "%s.%s.ldif"%(timestamp,fname)
	try:
		f = open("%s%s"%(env.LOGS,fname),'w')
		try:
			f.writelines(content)
		finally:
			f.close()
	except IOError:
		pass

def helper_create_netgroup(NETGROUP,env):
	dofile = undofile = error=""
        DN="ou=Netgroup," + env.BASEDN
        FILTER="(&(objectClass=nisnetgroup)(cn=" + NETGROUP + "))"
	ATTR = [ "cn" ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:
		result = "Generic error occured (are you logged in?)"
		return dofile, undofile, result
	connection.unbind()
	# if netgroup exists; error message, return
	if result == []:True
	else:
		if result[0][1]['cn'][0] == NETGROUP:
			error="ERROR: netgroup " + NETGROUP + " already exists!"
			return dofile, undofile, error	
	# else make (un)dofile
	dn="cn=" + NETGROUP + ",ou=Netgroup," + env.BASEDN
	entry={"objectClass": ["nisNetgroup", "top"], "cn": [NETGROUP]}
	dofile = ldif.CreateLDIF(dn,entry)
	undofile = ldif.CreateLDIF(dn,{"changetype": ("delete",)})
	return dofile, undofile, error

def helper_delete_netgroup(NETGROUP,env):
	dofile = undofile = error=""
	DN="ou=Netgroup," + env.BASEDN
	FILTER="(&(objectClass=nisnetgroup)(cn=" + NETGROUP + "))"
	ATTR=None
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:
                result = "Generic error occured (are you logged in?)"
                return dofile, undofile, result
        connection.unbind()
	# if netgroup does not exist; error message, return
	if result == []:
                error="ERROR: netgroup " + NETGROUP + " does not exists!"
                return dofile, undofile, error
	# else make (un)dofile
	for dn,entry in result:
	        undofile = ldif.CreateLDIF(dn,entry)
	DN="cn=" + NETGROUP + ",ou=Netgroup," + env.BASEDN
        entry={"objectClass": ["nisNetgroup", "top"], "cn": [NETGROUP]}
        dofile = ldif.CreateLDIF(DN,{"changetype": ("delete",)})
	return dofile, undofile, error

def helper_add_user_to_netgroup(NETGROUP, UID, env):
	dofile = undofile = error=""
        DN="ou=Netgroup," + env.BASEDN
        FILTER="(&(objectClass=nisNetgroup)(cn=" + NETGROUP + ")(nisNetgroupTriple=\(*," + UID + ",*\)))"
        ATTR=[ "cn" ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:
                result = "Generic error occured (are you logged in?)"
                return dofile, undofile, result
        connection.unbind()
	# if user already in netgroup, error message, return
	if result != []:
		error="ERROR: User " + UID + " already member of netgroup " + NETGROUP
		return dofile, undofile, error
        DN="ou=Netgroup," + env.BASEDN
        FILTER="(&(objectClass=nisnetgroup)(cn=" + NETGROUP + "))"
        ATTR=None
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:
                result = "Generic error occured (are you logged in?)"
                return dofile, undofile, result
        connection.unbind()
        # if netgroup does not exist; error message, return
        if result == []:
                error="ERROR: netgroup " + NETGROUP + " does not exists!"
                return dofile, undofile, error
        DN="ou=People," + env.BASEDN
        FILTER="(&(objectClass=posixAccount)(uid=" + UID + "))"
        ATTR=[ "cn" ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:
                result = "Generic error occured (are you logged in?)"
                return dofile, undofile, result
	connection.unbind()
        # if user does not exist; error message, return
        if result == []:
                error="ERROR: user " + UID + " does not exists!"
                return dofile, undofile, error
	# else make (un)dofile
	dofile = "dn: cn=" + NETGROUP + ",ou=Netgroup," + env.BASEDN + "\n"
	dofile += "changetype: modify\n"
	dofile += "add: nisNetgroupTriple\n"
	dofile += "nisNetgroupTriple: (-," + UID + ",)\n\n"
	undofile = "dn: cn=" + NETGROUP + ",ou=Netgroup," + env.BASEDN + "\n"
        undofile += "changetype: modify\n"
        undofile += "delete: nisNetgroupTriple\n"
        undofile += "nisNetgroupTriple: (-," + UID + ",)\n\n"
	return dofile, undofile, error

def helper_del_user_from_netgroup(NETGROUP, UID, env):
        dofile = undofile = error=""
        # if user does not exist; error message, return
        DN="ou=People," + env.BASEDN
        FILTER="(&(objectClass=posixAccount)(uid=" + UID + "))"
        ATTR=[ "cn" ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:
                result = "Generic error occured (are you logged in?)"
                return dofile, undofile, result
        connection.unbind()
        if result == []:
                error="ERROR: user " + UID + " does not exists!"
                return dofile, undofile, error
        # if netgroup does not exist; error message, return
        DN="ou=Netgroup," + env.BASEDN
        FILTER="(&(objectClass=nisnetgroup)(cn=" + NETGROUP + "))"
        ATTR=None
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        	connection.unbind()
        except ldap.LDAPError, e:
		error = "Generic error occured (are you logged in?)"
		return dofile,undofile,error
	if result == []:
                error="ERROR: netgroup " + NETGROUP + " does not exists!"
                return dofile, undofile, error
        # if user not in netgroup, error message, return
        DN="ou=Netgroup," + env.BASEDN
        FILTER="(&(objectClass=nisNetgroup)(cn=" + NETGROUP + ")(nisNetgroupTriple=\(*," + UID + ",*\)))"
        ATTR=[ "nisNetgroupTriple" ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        	connection.unbind()
        except ldap.LDAPError, e:
		error = "Generic error occured (are you logged in?)"
		return dofile,undofile,error
        
	if result == []:
                error="ERROR: " + UID + " is not a member of netgroup " + NETGROUP
                return dofile, undofile, error
	else:
		for dn,entry in result:
			for item in entry:
				for value in entry[item]:
					t = re.match( '((.*),' + UID + ',(.*))', (value), re.M|re.I)
					if t != None:
						nisNetgroupTriple = (value)
	# Build LDIFs
	dofile = "dn: cn=" + NETGROUP + ",ou=Netgroup," + env.BASEDN + "\n"
        dofile += "changetype: modify\n"
        dofile += "delete: nisNetgroupTriple\n"
        dofile += "nisNetgroupTriple: " + nisNetgroupTriple + "\n\n"
	undofile = "dn: cn=" + NETGROUP + ",ou=Netgroup," + env.BASEDN + "\n"
        undofile += "changetype: modify\n"
        undofile += "add: nisNetgroupTriple\n"
        undofile += "nisNetgroupTriple: " + nisNetgroupTriple + "\n\n"
	return dofile,undofile,error

def helper_del_host_from_netgroup(NETGROUP, HOST, env):                                 
        dofile = undofile = error = nisNetgroupTriple = "" 
	# If netgroup does not exist; error message, return                             
	DN="ou=Netgroup,%s"%(env.BASEDN)
	FILTER="(&(objectClass=nisnetgroup)(cn=%s))"%(NETGROUP)                         
	ATTR=None
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)              
		connection.unbind()
        except ldap.LDAPError, e:
		error = "Generic error occured (are you logged in?)"
		return dofile,undofile,error
	if result == []:
		error="ERROR: netgroup %s does not exists!"%(NETGROUP)                  
		return dofile, undofile, error
	# If host not in netgroup; error message, return                                
	DN="ou=Netgroup,%s"%(env.BASEDN)
	FILTER="(&(objectClass=nisNetgroup)(cn=%s)(nisNetgroupTriple=\(%s,,\)))"%(NETGROUP, HOST)    
	ATTR=[ "nisNetgroupTriple" ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
		connection.simple_bind_s() 
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)              
		connection.unbind()
        except ldap.LDAPError, e:
		error = "Generic error occured (are you logged in?)"
		return dofile,undofile,error
	if result == []:
		error="ERROR: %s is not a host in netgroup %s"%(HOST, NETGROUP)            
		return dofile, undofile, error                                          
	else:
		for dn,entry in result:
			for item in entry:
				for value in entry[item]:
					t = re.match( '\(%s,(.*),(.*)\)'%(HOST), (value), re.M|re.I)
					if t != None:
						nisNetgroupTriple = (value)
	dofile = "dn: cn=%s,%s\n"%(NETGROUP,DN)
	dofile += "changetype: modify\n"
	dofile += "delete: nisNetgroupTriple\n"
	dofile += "nisNetgroupTriple: %s\n\n"%(nisNetgroupTriple)
	undofile = "dn: cn=%s,%s\n"%(NETGROUP,DN)
	undofile += "changetype: modify\n"
	undofile += "add: nisNetgroupTriple\n"
	undofile += "nisNetgroupTriple: %s\n\n"%(nisNetgroupTriple)
	return dofile, undofile, error

def helper_add_host_to_netgroup(NETGROUP, HOST, env):
	dofile = undofile = error = nisNetgroupTriple = "" 
	# If netgroup does not exist; error message, return                             
	DN="ou=Netgroup,%s"%(env.BASEDN)
	FILTER="(&(objectClass=nisnetgroup)(cn=%s))"%(NETGROUP)                         
	ATTR=None
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)              
		connection.unbind()
        except ldap.LDAPError, e:
		error = "Generic error occured (are you logged in?)"
		return dofile,undofile,error
	if result == []:
		error="ERROR: netgroup %s does not exists!"%(NETGROUP)                  
		return dofile, undofile, error
	# If host not in netgroup; error message, return                                
	DN="ou=Netgroup,%s"%(env.BASEDN)
	FILTER="(&(objectClass=nisNetgroup)(cn=%s)(nisNetgroupTriple=\(%s,,\)))"%(NETGROUP, HOST)    
	ATTR=[ "nisNetgroupTriple" ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
		connection.simple_bind_s() 
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)              
		connection.unbind()
        except ldap.LDAPError, e:
		error = "Generic error occured (are you logged in?)"
		return dofile,undofile,error
	if result != []:
		error="ERROR: host %s already in netgroup %s"%(HOST, NETGROUP)            
		return dofile, undofile, error                                          
	dofile = "dn: cn=%s,%s\n"%(NETGROUP,DN)
	dofile += "changetype: modify\n"
	dofile += "add: nisNetgroupTriple\n"
	dofile += "nisNetgroupTriple: (%s,,)\n\n"%(HOST)
	undofile = "dn: cn=%s,%s\n"%(NETGROUP,DN)
	undofile += "changetype: modify\n"
	undofile += "delete: nisNetgroupTriple\n"
	undofile += "nisNetgroupTriple: (%s,,)\n\n"%(HOST)
	return dofile, undofile, error

def helper_add_netgroup_to_netgroup(PARENT, CHILD, env):
	dofile = undofile = error = ""
	# If netgroup does not exist; error message, return                             
	DN="ou=Netgroup,%s"%(env.BASEDN)
	FILTER1="(&(objectClass=nisnetgroup)(cn=%s))"%(PARENT)                         
	FILTER2="(&(objectClass=nisnetgroup)(cn=%s))"%(CHILD)                         
	FILTER3="(&(objectClass=nisnetgroup)(cn=%s)(memberNisNetgroup=%s))"%(PARENT, CHILD)                         
	ATTR=None
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
		connection.simple_bind_s()
		result1 = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER1, ATTR)              
		result2 = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER2, ATTR)              
		result3 = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER3, ATTR)              
		connection.unbind()
        except ldap.LDAPError, e:
		error = "Generic error occured (are you logged in?)"
		return dofile,undofile,error
	if result1 == []:
		error="ERROR: netgroup %s does not exists!"%(PARENT)                  
		return dofile, undofile, error
	if result2 == []:
		error="ERROR: netgroup %s does not exists!"%(CHILD)                  
		return dofile, undofile, error
	if result3 != []:
		error="ERROR: netgroup %s is already a member of %s!"%(CHILD, PARENT)
		return dofile, undofile, error
	if CHILD == PARENT:
		error="ERROR: Netgroup %s cannot be a member of itself!"%(PARENT)
	dofile = "dn: cn=%s,%s\n"%(PARENT, DN)
	dofile += "changetype: modify\n"
	dofile += "add: memberNisNetgroup\n"
	dofile += "memberNisNetgroup: %s\n"%(CHILD)
	undofile = "dn: cn=%s,%s\n"%(PARENT, DN)
	undofile += "changetype: modify\n"
	undofile += "delete: memberNisNetgroup\n"
	undofile += "memberNisNetgroup: %s\n"%(CHILD)
	return dofile, undofile, error

def helper_del_netgroup_from_netgroup(PARENT, CHILD, env):
	dofile = undofile = error = ""
	# If netgroup does not exist; error message, return                             
	DN="ou=Netgroup,%s"%(env.BASEDN)
	FILTER1="(&(objectClass=nisnetgroup)(cn=%s))"%(PARENT)                         
	FILTER2="(&(objectClass=nisnetgroup)(cn=%s)(memberNisNetgroup=%s))"%(PARENT, CHILD)                         
	ATTR=None
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
		connection.simple_bind_s()
		result1 = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER1, ATTR)              
		result2 = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER2, ATTR)              
		connection.unbind()
        except ldap.LDAPError, e:
		error = "Generic error occured (are you logged in?)"
		return dofile,undofile,error
	if result1 == []:
		error="ERROR: netgroup %s does not exists!"%(PARENT)                  
		return dofile, undofile, error
	if result2 == []:
		error="ERROR: netgroup %s is not a member of %s!"%(CHILD, PARENT)                  
		return dofile, undofile, error
	dofile = "dn: cn=%s,%s\n"%(PARENT, DN)
	dofile += "changetype: modify\n"
	dofile += "delete: memberNisNetgroup\n"
	dofile += "memberNisNetgroup: %s\n"%(CHILD)
	undofile = "dn: cn=%s,%s\n"%(PARENT, DN)
	undofile += "changetype: modify\n"
	undofile += "add: memberNisNetgroup\n"
	undofile += "memberNisNetgroup: %s\n"%(CHILD)
	return dofile, undofile, error

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

def create_netgroup(env, screen):
	# ARGUMENTS: NETGROUP
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	s.keypad(1)
        # Setup colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
        s.addstr(2, 2, "Add new netgroup", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter netgroup: ", curses.color_pair(1))
	curses.echo()
        NETGROUP = getInput(s, 4, 18, 58, 1, True)
        if NETGROUP == "":
		s.erase()
		return
	dofile, undofile, error = helper_create_netgroup(NETGROUP,env)
	if error != "":
		s.addstr(6, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))      
		s.getch()
		s.erase()
		return
	content,error=apply_ldif.ldif2dict(dofile)
	if error != "OK":print error
	else:
		try:
			error=apply_ldif.apply_ldif(content,env)
        		WriteLog(dofile, "create_netgroup.done.%s"%(NETGROUP), env)
        		WriteLog(undofile, "create_netgroup.undo.%s"%(NETGROUP), env)
			s.addstr(6, 2, "Netgroup %s created."%(NETGROUP), curses.color_pair(2))
			s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))      
			s.getch()
		except:
                	s.addstr(6, 2, str(error), n)
			s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))      
			s.getch()
        s.erase()
	return 

def delete_netgroup(env, screen):
	# ARGUMENTS: NETGROUP
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	s.keypad(1)
        # Setup colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Delete netgroup", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter netgroup: ", curses.color_pair(1))
        NETGROUP = getInput(s, 4, 18, 58, 1, True)
        if NETGROUP == "":
		s.erase()
		return
	dofile, undofile, error = helper_delete_netgroup(NETGROUP,env)
        if error != "":
                s.addstr(6, 2, error, curses.color_pair(2))
        	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
		s.getch()
		s.erase()
                return
        content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":print error
        else:
        	error=apply_ldif.apply_ldif(content,env)
        	WriteLog(dofile, "delete_netgroup.done.%s"%(NETGROUP), env)
        	WriteLog(undofile, "delete_netgroup.undo.%s"%(NETGROUP), env)
        if error != "":
                s.addstr(6, 2, str(error), curses.color_pair(2))
        	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
		s.getch()
		s.erase()
                return
	else:
		s.addstr(6, 2, "Netgroup '" + NETGROUP + "' deleted.", curses.color_pair(2))
        	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return

def add_user_to_netgroup(env, screen):
	# ARGUMENTS: NETGROUP, UID
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	s.keypad(1)
        # Setup colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Link user to netgroup", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
        UID = getInput(s, 4, 18, 58, 1, True)
        if UID == "":
		s.erase()
		return
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(5, 2, "Enter netgroup: ", curses.color_pair(1))
	NETGROUP = getInput(s, 5, 18, 58, 1, True)
        if NETGROUP == "":
		s.erase()
		return
	dofile, undofile, error = helper_add_user_to_netgroup(NETGROUP,UID,env)
        if error != "":
                s.addstr(7, 2, error, curses.color_pair(2))
        	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
	content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":print error
        else:
        	error=apply_ldif.apply_ldif(content,env)
        	WriteLog(dofile, "delete_user_from_netgroup.done.%s-%s"%(UID,NETGROUP), env)
        	WriteLog(undofile, "delete_user_from_netgroup.undo.%s-%s"%(UID,NETGROUP), env)
        if error != "":
                s.addstr(7, 2, str(error), curses.color_pair(2))
        	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
        else:
                s.addstr(7, 2, "User '" + UID + "' added to netgroup " + NETGROUP + ".", curses.color_pair(2))
	curses.noecho()
        s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
        s.getch()
	s.erase()
        return

def del_user_from_netgroup(env,screen):
	# ARGUMENTS: NETGROUP, UID
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
        # Setup colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	s.box()        
        s.addstr(2, 2, "Unlink user from netgroup", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
        UID = getInput(s, 4, 18, 58, 1, True)
        if UID == "":
		s.erase()
		return
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(5, 2, "Enter netgroup: ", curses.color_pair(1))
	NETGROUP = getInput(s, 5, 18, 58, 1, True)
        if NETGROUP == "":
		s.erase()
		return
        dofile, undofile, error = helper_del_user_from_netgroup(NETGROUP,UID,env)
        if error != "":
                s.addstr(7, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
	content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":print error
        else:
        	error=apply_ldif.apply_ldif(content,env)
        	WriteLog(dofile, "add_user_to_netgroup.done.%s-%s"%(UID,NETGROUP), env)
        	WriteLog(undofile, "add_user_to_netgroup.undo.%s-%s"%(UID,NETGROUP), env)
        if error != "":
                s.addstr(7, 2, str(error), curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
        else:
                s.addstr(7, 2, "User '" + UID + "' deleted from netgroup " + NETGROUP + ".", curses.color_pair(2))
        curses.noecho()
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
        s.getch()
	s.erase()
        return

def del_host_from_netgroup(env, screen):
	# ARGUMENTS: NETGROUP, UID
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
        # Setup colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	s.box()        
        s.addstr(2, 2, "Unlink host from netgroup", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter hostname: ", curses.color_pair(1))
        HOST = getInput(s, 4, 18, 58, 1, True)
        if HOST == "":
		s.erase()
		return
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(5, 2, "Enter netgroup: ", curses.color_pair(1))
	NETGROUP = getInput(s, 5, 18, 58, 1, True)
        if NETGROUP == "":
		s.erase()
		return
        dofile, undofile, error = helper_del_host_from_netgroup(NETGROUP, HOST, env)
        if error != "":
                s.addstr(7, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
	content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":print error
        else:
        	error=apply_ldif.apply_ldif(content,env)
        	WriteLog(dofile, "del_host_from_netgroup.done.%s-%s"%(HOST,NETGROUP), env)
        	WriteLog(undofile, "del_host_from_netgroup.undo.%s-%s"%(HOST,NETGROUP), env)
        if error != "":
                s.addstr(7, 2, str(error), curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
        else:
                s.addstr(7, 2, "Host '" + HOST + "' deleted from netgroup " + NETGROUP + ".", curses.color_pair(2))
        curses.noecho()
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
        s.getch()
	s.erase()
        return

def add_host_to_netgroup(env, screen):
	# ARGUMENTS: NETGROUP, UID
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
        # Setup colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	s.box()        
        s.addstr(2, 2, "Link host to netgroup", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter hostname: ", curses.color_pair(1))
        HOST = getInput(s, 4, 18, 58, 1, True)
        if HOST == "":
		s.erase()
		return
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(5, 2, "Enter netgroup: ", curses.color_pair(1))
	NETGROUP = getInput(s, 5, 18, 58, 1, True)
        if NETGROUP == "":
		s.erase()
		return
        dofile, undofile, error = helper_add_host_to_netgroup(NETGROUP, HOST, env)
        if error != "":
                s.addstr(7, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
	content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":print error
        else:
        	error=apply_ldif.apply_ldif(content,env)
        	WriteLog(dofile, "add_host_to_netgroup.done.%s-%s"%(HOST,NETGROUP), env)
        	WriteLog(undofile, "add_host_to_netgroup.undo.%s-%s"%(HOST,NETGROUP), env)
        if error != "":
                s.addstr(7, 2, str(error), curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
        else:
                s.addstr(7, 2, "Host '" + HOST + "' added to netgroup " + NETGROUP + ".", curses.color_pair(2))
        curses.noecho()
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
        s.getch()
	s.erase()
        return

def del_netgroup_from_netgroup(env, screen):
	# ARGUMENTS: NETGROUP, UID
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
        # Setup colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	s.box()        
        s.addstr(2, 2, "Unlink netgroup from netgroup", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter parent netgroup: ", curses.color_pair(1))
        PARENT = getInput(s, 4, 25, 51, 1, True)
        if PARENT == "":
		s.erase()
		return
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(5, 2, "Enter child netgroup:  ", curses.color_pair(1))
	CHILD = getInput(s, 5, 25, 51, 1, True)
        if CHILD == "":
		s.erase()
		return
        dofile, undofile, error = helper_del_netgroup_from_netgroup(PARENT, CHILD, env)
        if error != "":
                s.addstr(7, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
	content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":
                s.addstr(7, 2, str(error), curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
	else:
        	error=apply_ldif.apply_ldif(content,env)
		if error == "OK":
        		WriteLog(dofile, "del_netgroup_from_netgroup.done.%s-%s"%(CHILD, PARENT), env)
	        	WriteLog(undofile, "del_netgroup_from_netgroup.undo.%s-%s"%(CHILD, PARENT), env)
        		s.addstr(7, 4, ": Netgroup %s deleted from netgroup %s."%(CHILD, PARENT), curses.color_pair(2))
	s.addstr(7, 2, str(error), curses.color_pair(2))
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return	

def add_netgroup_to_netgroup(env, screen):
	# ARGUMENTS: NETGROUP, UID
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
        # Setup colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	s.box()        
        s.addstr(2, 2, "Link netgroup to netgroup", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(4, 2, "Enter parent netgroup: ", curses.color_pair(1))
        PARENT = getInput(s, 4, 25, 51, 1, True)
        if PARENT == "":
		s.erase()
		return
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
        s.addstr(5, 2, "Enter child netgroup:  ", curses.color_pair(1))
	CHILD = getInput(s, 5, 25, 51, 1, True)
        if CHILD == "":
		s.erase()
		return
        dofile, undofile, error = helper_add_netgroup_to_netgroup(PARENT, CHILD, env)
        if error != "":
                s.addstr(7, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
	content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":
                s.addstr(7, 2, str(error), curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
                s.getch()
		s.erase()
                return
	else:
        	error=apply_ldif.apply_ldif(content,env)
		if error == "OK":
        		WriteLog(dofile, "add_netgroup_to_netgroup.done.%s-%s"%(CHILD, PARENT), env)
	        	WriteLog(undofile, "add_netgroup_to_netgroup.undo.%s-%s"%(CHILD, PARENT), env)
        		s.addstr(7, 4, ": Netgroup %s added to netgroup %s."%(CHILD, PARENT), curses.color_pair(2))
	s.addstr(7, 2, str(error), curses.color_pair(2))
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return	

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Add or remove (a user to/from) a group.')

        group1 = parser.add_mutually_exclusive_group(required=True)
        group1.add_argument('--add', action='store_true', default=False, help='Add a user to a group or add a new group.')
        group1.add_argument('--del', action='store_true', default=False, help='Delete a user from a group or delete a group.')

        group2 = parser.add_mutually_exclusive_group(required=True)
        group2.add_argument('-u', nargs=2, action='store', metavar=('user', 'group'), help='username groupname')
        group2.add_argument('-g', nargs=1, action='store', metavar=('group'), help='groupname') 

        parser.add_argument('--host', action='store', metavar='hostname', required=True, help='LDAP servername or ip-adress.')
	parser.add_argument('--binddn', action='store', metavar='dn', required=True, help='Distinguist name of bind user.')
	parser.add_argument('--basedn', action='store', metavar='dn', required=True, help='Base search DN.')
        parser.add_argument('-W', action='store_true', default=False, dest='passwordprompt', required=True, help='Prompt for bind password.')

	args = vars(parser.parse_args())

        add = args['add']
        delete = args['del']

	env=environment()
	env.LDAPSERVER = args['host']
	env.BINDDN = args['binddn']
	env.BASEDN = args['basedn']
	env.LDAPPW = args['passwordprompt']
	
        if args['passwordprompt'] == False:
                error = "ERROR: No bind password provided."
                print error
                exit(1)

        if args['passwordprompt']:
                print env.BINDDN
                env.LDAPPW = getpass.getpass()


        if add:
                if args['g'] == None:
			dofile, undofile,error = helper_add_user_to_netgroup(args['u'][1],args['u'][0],env)
                else:
			dofile,undofile,error = helper_create_netgroup(args['g'][0],env)
        else:           
                if args['g'] == None:
			dofile, undofile,error = helper_del_user_from_netgroup(args['u'][1],args['u'][0],env)
                else:
			dofile, undofile,error = helper_delete_netgroup(args['g'][0],env)

	if error =="":content,error=apply_ldif.ldif2dict(dofile)
	else:print error; sys.exit(1)
	if error =="OK":error=apply_ldif.apply_ldif(content,env)
	else:print error; sys.exit(1)
	if error !="OK":print error

        sys.exit(1)
