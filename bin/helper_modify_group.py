#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 Robert Nagtegaal <masikh@gmail.com>
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import argparse,curses,getpass,ldap,ldif,string,sys,time
import helper_apply_ldif as apply_ldif
from copy import deepcopy
from os import system

class environment():
	LDAPSERVER = BASEDN = BINDDN = LDAPPW = ""
	LDBUG = False
	VERBOSE = False
	def group_ranges(self, typeset):
		self.ranges = { 'primairy': ['100','999'],
				'secondairy': ['11100', '13999'] }
		return self.ranges[typeset][0],self.ranges[typeset][1]

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

def isGroup(GROUP, env):
	error="OK"
	DN="ou=Group," + env.BASEDN
        FILTER="(&(objectClass=posixGroup)(cn=" + GROUP + "))"
        ATTR = [ "memberUid" ]
        try:
        	connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, error:return error, True
        if result == []:return error, False
	else:return error, True

def isUser(UID, env):
        error="OK"
        DN="ou=People," + env.BASEDN
        FILTER="(&(objectClass=posixAccount)(uid=" + UID + "))"
        ATTR = [ "uid" ]
        try:
                connection = ldap.open(env.LDAPSERVER)
                connection.simple_bind_s()
                result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, error:return error, True
	if result == []:return error, False
        else:return error, True

def isInGroup(UID, GROUP, env):
	error = "OK"
        DN="ou=Group," + env.BASEDN
        FILTER="(&(cn=%s)(memberUid=%s))"%(GROUP,UID)
        ATTR = [ "cn" ]
	try:
		connection = ldap.open(env.LDAPSERVER)
	        connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, error: return "Generic error occured (are you logged in?)", None
        if result == []:return error, False
	else:return error, True

def helper_get_gidNumber(GROUP, env):
	error="OK"
	DN="ou=Group," + env.BASEDN
	FILTER="(&(objectClass=posixGroup)(cn=" + GROUP + "))"
	ATTR = [ "gidNumber" ]
	try:
		connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, error:return "Generic error occured (are you logged in?)", "0"
	if result == []:return "No such group", "0"
	else:
		for dn,entry in result:
			value =  entry['gidNumber'][0]
		return error, value

def helper_get_memberUID(GROUP, env):
	error="OK"
	DN="ou=Group," + env.BASEDN
	FILTER="(&(objectClass=posixGroup)(cn=" + GROUP + "))"
	ATTR = [ "memberUid" ]
	try:
		connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, error:return "Generic error occured (are you logged in?)", "0"
	if result == []:return "No such group", "0"
	else:
		value = []
		for dn,entry in result:
			try:value =  entry['memberUid']
			except:continue
		return error, value


def helper_get_group_attr(attributes, GROUP, env):
	error = "OK"
	DN="ou=Group,%s"%(env.BASEDN)
	FILTER="(&(objectClass=posixGroup)(cn=%s))"%(GROUP)
	ATTR = None 
	try:
		connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
		temp = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, error:return "Generic error occured (are you logged in?)", "0"
	result = temp[0][1]
	result.setdefault('userPassword',str("{crypt}*"))
	del result['objectClass']
	result['gidNumber'] = result['gidNumber'][0]
	result['cn'] = result['cn'][0]
	return error, result

def helper_modify_group_attr(selection, pos, modified, screen, env):
	alfabet = 1
	if selection == "cn":alfabet = 4 
	if selection == "gidNumber":alfabet = 3
	if selection == "userPassword":alfabet = 5
	screen.addstr(pos, 20, " "*56)
	screen.addstr(pos, 20, "")
	result = getInput(screen, pos, 20, 56, alfabet, True)
	if result != "":modified[selection] = result
	return modified

def helper_commit_modify_group(GROUP, result, modified, env):
	error = "OK"
	dofile = undofile = ""
	if result['cn'] != modified['cn']:
		dofile += "dn: cn=%s,ou=Group,%s\n"%(GROUP,env.BASEDN)
		dofile += "changetype: moddn\n"
		dofile += "newrdn: cn=%s\n"%(modified['cn'])
		dofile += "deleteoldrdn: 1\n\n"
		undofile += "dn: cn=%s,ou=Group,%s\n"%(modified['cn'],env.BASEDN)
		undofile += "changetype: moddn\n"
		undofile += "newrdn: cn=%s\n"%(GROUP)
		undofile += "deleteoldrdn: 1\n\n"
	if result['gidNumber'] != modified['gidNumber']:
		dofile += "dn: cn=%s,ou=Group,%s\n"%(modified['cn'],env.BASEDN)
		dofile += "changetype: modify\n"
		dofile += "replace: gidNumber\n"
		dofile += "gidNumber: %s\n\n"%(modified['gidNumber'])
		undofile += "dn: cn=%s,ou=Group,%s\n"%(modified['cn'],env.BASEDN)
		undofile += "changetype: modify\n"
		undofile += "replace: gidNumber\n"
		undofile += "gidNumber: %s\n\n"%(result['gidNumber'])
	if result['userPassword'] != modified['userPassword']:
		dofile += "dn: cn=%s,ou=Group,%s\n"%(modified['cn'],env.BASEDN)
		dofile += "changetype: modify\n"
		dofile += "replace: userPassword\n"
		dofile += "userPassword: %s\n\n"%(modified['userPassword'])
		undofile += "dn: cn=%s,ou=Group,%s\n"%(modified['cn'],env.BASEDN)
		undofile += "changetype: modify\n"
		undofile += "replace: userPassword\n"
		undofile += "userPassword: %s\n\n"%(result['userPassword'])
	content,error=apply_ldif.ldif2dict(dofile)
	if error != "OK":return error
	error=apply_ldif.apply_ldif(content,env)
	WriteLog(dofile, "modify_grp.done.%s"%(GROUP), env)
	WriteLog(undofile, "modify_grp.undo.%s"%(GROUP), env)
	return error

def helper_modify_group(GROUP, screen, env):
	error = "OK"
	error, exist = isGroup(GROUP, env)
	if not exist:return "ERROR: Group %s does not exist!"%(GROUP) 
	screen.erase()
	screen.box()
	screen.addstr(2,2, "Modifying group %s"%(GROUP), curses.color_pair(3))
	attributes = ["cn","gidNumber","userPassword"]
	length = len(attributes)
	error, result = helper_get_group_attr(attributes, GROUP, env)
	modified = deepcopy(result)
	if error != "OK":return error
	escape = False
	pos = 0 
	selection = ""
	screen.addstr(19,2, "[Use [ESC] when done or to quit, [arrow] selects item, [enter] modify item]", curses.color_pair(1))
	while not escape:
		i = 4
		for attribute in attributes:
			if modified[attribute] != result[attribute]:
				screen.addstr(i, 1, "*", curses.color_pair(1))
			else:
				screen.addstr(i, 1, " ", curses.color_pair(2))
			screen.addstr(i, 20, " "*56, curses.color_pair(2))
			if pos + 4 == i:
				screen.addstr(i, 2, attribute, curses.color_pair(1))
				screen.addstr(i, 20, modified[attribute], curses.color_pair(1))
				selection = attribute
			else:
				screen.addstr(i, 2, attribute, curses.color_pair(2))
				screen.addstr(i, 20, modified[attribute], curses.color_pair(2))
			i += 1
		screen.refresh()
		x = screen.getch()
		screen.addstr(19,2, "[Use [ESC] when done or to quit, [arrow] selects item, [enter] modify item]", curses.color_pair(1))
		if x == 27 or x == 263:
			escape = True
		elif x == 258 and pos < length - 1:pos += 1
		elif x == 259 and pos > 0:pos -= 1
		elif x == ord('\n'):
			free = False
			modified = helper_modify_group_attr(selection, pos + 4, modified, screen, env)
			if modified['gidNumber'] != result['gidNumber']:
				error, free = helper_free_gid(modified['gidNumber'], env)
				if error != "OK": return error
				if not free:
					screen.addstr(19, 2, "[Error: gidNumber '%s' is not free!]"%(modified['gidNumber']), curses.color_pair(1))
					modified['gidNumber'] = result['gidNumber']
	screen.hline(19, 2, curses.ACS_HLINE, 75)
	if result != modified:
		screen.addstr(8, 2, "Do you wish to commit changes? [y|[n]]", curses.color_pair(1))
		selection = getInput(screen, 8, 2, 1, 1, False)
		if selection == 'y' or selection == 'Y':
			error = helper_commit_modify_group(GROUP, result, modified, env)
			if error == "OK": return "Group %s modified succesfully."%(GROUP)
	return error

def add_group(GROUP, next_free, env):
	dofile = "dn: cn=%s,ou=Group,%s\n" % (GROUP,env.BASEDN)
	dofile += "objectClass: posixGroup\n"
	dofile += "objectClass: top\n"
	dofile += "cn: %s\n" % (GROUP)
	dofile += "userPassword: {crypt}*\n"
	dofile += "gidNumber: %s\n\n" % (next_free)
	undofile = "dn: cn=%s,ou=Group,%s\n" % (GROUP,env.BASEDN)
	undofile += "changetype: delete\n\n"
	return dofile,undofile

def add_user(UID, GROUP, env):
	dofile = "dn: cn=%s,ou=Group,%s\n" % (GROUP,env.BASEDN)
	dofile += "changetype: modify\n"
	dofile += "add: memberUid\n"
	dofile += "memberUid: %s\n\n" % (UID)
	undofile = "dn: cn=%s,ou=Group,%s\n" % (GROUP,env.BASEDN)
	undofile += "changetype: delete\n"
	undofile += "delete: memberUid\n"
	undofile += "memberUid: %s\n\n" % (UID)
	return dofile,undofile

def del_group(GROUP, gidNumber, result, env):
	dofile = "dn: cn=%s,ou=Group,%s\n" % (GROUP,env.BASEDN)
	dofile += "changetype: delete\n\n"
	undofile = "dn: cn=%s,ou=Group,%s\n" % (GROUP,env.BASEDN)
	undofile += "objectClass: posixGroup\n"
	undofile += "objectClass: top\n"
	undofile += "cn: %s\n" % (GROUP)
	undofile += "userPassword: {crypt}*\n"
	undofile += "gidNumber: %s\n" % (gidNumber)
	if result != []:
		for item in result:
			undofile += "memberUid: %s\n" % (item)
	undofile += "\n"
	return dofile,undofile

def del_user(UID, GROUP, env):
	dofile = "dn: cn=%s,ou=Group,%s\n" % (GROUP,env.BASEDN)
	dofile += "changetype: modify\n"
	dofile += "delete: memberUid\n"
	dofile += "memberUid: %s\n\n" % (UID)
	undofile = "dn: cn=%s,ou=Group,%s\n" % (GROUP,env.BASEDN)
	undofile += "changetype: modify\n"
	undofile += "add: memberUid\n"
	undofile += "memberUid: %s\n\n" % (UID)
	return dofile,undofile

def helper_next_free(TYPE, env):
	error = "OK"
	toprange = highest = 0
	DN="ou=Group," + env.BASEDN
	FILTER="(cn=*)"
	ATTR=["gidNumber"]
	try:begin,end=env.group_ranges(TYPE)
	except:begin=end=100
	try:
		connection = ldap.open(env.LDAPSERVER)
        	connection.simple_bind_s()
 		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, error: return error, toprange 
	connection.unbind()
	for dn,entry in result:
		current=entry[ATTR[0]][0]
		# get highest of all
		if (int(highest) < int(current)):highest=current
		# get highest in range
		if (int(current) < int(begin)):continue
		elif (int(current) > int(end)):continue
		elif (int(current) >= int(toprange)):toprange=current
	if (int(toprange) == int(end)):toprange=int(highest) + 1
	elif (int(toprange) == 0):toprange=int(highest) + 1
	else: toprange = int(toprange) + 1
	return error, toprange

def helper_free_gid(gidNumber, env):
	error = "OK"
	DN="ou=Group,%s"%(env.BASEDN)
	FILTER="(&(objectClass=posixGroup)(gidNumber=%s))"%(gidNumber)
	ATTR = ["cn"]
	try:	
		connection = ldap.open(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, e:return error, False
	if result == []:return error, True
	else: return error, False

def helper_add_group(GROUP, TYPE, env):
	error = "OK"
	error,next_free = helper_next_free(TYPE, env)
	if error != "OK":return "Generic error occured (are you logged in?)"
	error,result = isGroup(GROUP, env)
	if error != "OK":return "Generic error occured (are you logged in?)"
	if result == False:
		dofile,undofile = add_group(GROUP,next_free,env)
		content,error=apply_ldif.ldif2dict(dofile)
		if error != "OK":return error
		error=apply_ldif.apply_ldif(content,env)
		WriteLog(dofile, "add_grp.done.%s"%(GROUP), env)
		WriteLog(undofile, "add_grp.undo.%s"%(GROUP), env)
	else:error = "Group %s already exist!" % (GROUP)
	return error

def helper_del_group(GROUP,env):
	error,gidNumber = helper_get_gidNumber(GROUP, env)
	if error != "OK":return error
	error,result = helper_get_memberUID(GROUP, env)
	if error != "OK":return error
	dofile,undofile = del_group(GROUP, gidNumber, result, env)
	content,error=apply_ldif.ldif2dict(dofile)
	if error != "OK":return error
	error=apply_ldif.apply_ldif(content,env)
	WriteLog(dofile, "del_grp.done.%s"%(GROUP), env)
	WriteLog(undofile, "del_grp.undo.%s"%(GROUP), env)
	return error

def helper_add_user(UID, GROUP, env):
	error = "OK"
	error,isgroup = isGroup(GROUP, env)
        if error != "OK":return "Generic error occured (are you logged in?)"
	error,isuser = isUser(UID, env)
	if error != "OK":return "Generic error occured (are you logged in?)"
	error,isingroup = isInGroup(UID, GROUP, env)
	if error != "OK":return "Generic error occured (are you logged in?)"
	if isgroup == False:return "Group %s does not exist!" % (GROUP)
	if isuser == False:return "User %s does not exist!" % (UID)
	if isingroup == True:return "User %s already in group %s" % (UID, GROUP)
	if isgroup == True and isuser == True and isingroup == False:
		dofile,undofile = add_user(UID, GROUP, env)
		content,error=apply_ldif.ldif2dict(dofile)
		if error != "OK":return error
		error=apply_ldif.apply_ldif(content,env)
		WriteLog(dofile, "add_user_to_grp.done.%s-%s"%(UID,GROUP), env)
		WriteLog(undofile, "add_user_to_grp.undo.%s-%s"%(UID,GROUP), env)
	return error

def helper_del_user(UID, GROUP,env):
	error = "OK"
	error,isgroup = isGroup(GROUP, env)
	if error != "OK":return "Generic error occured (are you logged in?)"
	error,isuser = isUser(UID, env)
	if error != "OK":return "Generic error occured (are you logged in?)"
	error,isingroup = isInGroup(UID, GROUP, env)
	if error != "OK":return "Generic error occured (are you logged in?)"
	if isuser == False:return "User %s does not exist!" % (UID)
        if isgroup == False:return "Group %s does not exist!" % (GROUP)
	if isingroup == False:return "User %s is not a member of group %s!" % (UID,GROUP)
	dofile,undofile = del_user(UID, GROUP, env)
	content,error=apply_ldif.ldif2dict(dofile)
	if error != "OK":return error
	else:error=apply_ldif.apply_ldif(content,env)
	WriteLog(dofile, "del_user_to_grp.done.%s-%s"%(UID,GROUP), env)
	WriteLog(undofile, "del_user_to_grp.undo.%s-%s"%(UID,GROUP), env)
	return error

def getInput(screen,offset_y,offset_x,length,alfabet,cursor):
        allowed = {     0 : (set("y" + "Y" + "n" + "N"),
                            "Use yY/nN only!"),
                        1 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+"),
                            "Use -_.+ a-z A-Z 0-9 only"),
                        2 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+" + "=" + ","),
                            "Use -_.+=, a-z A-Z 0-9 only"),
                        3 : (set(string.digits),
                            "Use 0-9 only"),
                        4 : (set(string.digits + string.ascii_lowercase + "-" + "_" + "." + "+"),
                            "Use 0-9 a-z -_.+ only"),
                        5 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+" + "=" + "," + "{" + "}" + "*"),
                            "Use 0-9 a-z A-Z -_.+=,{}* only")
                  }
        wy,wx=screen.getmaxyx()
        i = 0
        value = ""
        while True:
                if cursor:curses.curs_set(1)
		else: curses.curs_set(0)
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
                        screen.addstr(wy - 1, 2,"(No more than %s characters allowed)"%(length),curses.color_pair(    1))
                        screen.addstr(offset_y, offset_x, "%s"%(value))
                        continue
		elif length == 1:
			value = string_x
			curses.curs_set(0)
			return value
                else:value += string_x
                screen.addstr(offset_y, offset_x, "%s"%(" "*length))
                screen.addstr(offset_y, offset_x, "%s"%(value))
                x = ""
                i += 1
        curses.curs_set(0)
        return value

def GUI_add_group(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.keypad(1)
	s.erase()
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Add new group", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter group:    ", curses.color_pair(1))
	GROUP = getInput(s,4,18,58,1,True)
	if GROUP == "":
		s.clear()
		return
	s.addstr(5, 2, "Is this group a primairy group?: [y/n]", curses.color_pair(1))
	TYPE = getInput(s,5,41,1,0,False)
	if TYPE == "":
		s.erase()
		return
	elif TYPE == "y" or TYPE == "Y":TYPE = "primairy"
	else:TYPE = "secondairy"
	error = helper_add_group(GROUP, TYPE, env)
	s.addstr(7, 2, error, curses.color_pair(2))
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return

def GUI_del_group(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
        s.box()
	s.addstr(2, 2, "Delete group", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter group:    ", curses.color_pair(1))
	GROUP = getInput(s,4,18,58,1,True)
	if GROUP == "":
		s.erase()
		return
	error = helper_del_group(GROUP,env)
	s.addstr(6, 2, error, curses.color_pair(2))
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return

def GUI_modify_group(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
        s.box()
	s.addstr(2, 2, "Modify group attributes", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter group:    ", curses.color_pair(1))
	GROUP = getInput(s,4,18,58,1,True)
	if GROUP == "":
		s.erase()
		return
	error = helper_modify_group(GROUP, s, env)
	if error != "OK":
		s.addstr(10, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
		s.getch()
	s.erase()
	return

def GUI_add_user(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	s.erase()
        s.box()
	s.addstr(2, 2, "Link user to group", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
	UID = getInput(s,4,18,58,1,True)
	if UID == "":
		s.erase()
		return
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(5, 2, "Enter group:    ", curses.color_pair(1))
	GROUP = getInput(s,5,18,58,1,True)
	if GROUP == "":
		s.erase()
		return
	error = helper_add_user(UID, GROUP, env)
	s.addstr(7, 2, error, curses.color_pair(2))
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return

def GUI_del_user(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	s.keypad(1)
	s.erase()
        s.box()
	s.addstr(2, 2, "Unlink user from group", curses.color_pair(3))

	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
	UID = getInput(s,4,18,58,1,True)
	if UID == "":
		s.erase()
		return
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(2))
	s.addstr(5, 2, "Enter group:    ", curses.color_pair(1))
	GROUP = getInput(s,5,18,58,1,True)
	if GROUP == "":
		s.erase()
		return
	error = helper_del_user(UID, GROUP, env)
	s.addstr(7, 2, error, curses.color_pair(2))
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Add or remove (a user to/from) a group.')

	group1 = parser.add_mutually_exclusive_group(required=True)
	group1.add_argument(   '--add',
				action='store_true',
				default=False,
				help='Add a user to a group or add a new group.')
	group1.add_argument(   '--del',
				action='store_true',
				default=False,
				help='Delete a user from a group or delete a group.')

	group2 = parser.add_mutually_exclusive_group(required=True)
	group2.add_argument(   '-u',
				nargs=2,
				action='store',
				metavar=('user', 'group'),
				help='username groupname')
        group2.add_argument(   '-g',
				nargs='+',
				action='store',
				metavar=('group [{pri,sec}]'),
				help='groupname [{pri,sec}]')
	choices = ['primairy','secondairy']
	
	parser.add_argument(  '--password',
				action='store',
				metavar='password',
				default="",
				help='A clear text password (Not needed!).')
	parser.add_argument(  '--host',
				action='store',
				metavar='hostname',
				help='LDAP servername or ip-adress.')
	parser.add_argument(  '--basedn',
				action='store',
				metavar='dn',
				help='Base search DN.')
	parser.add_argument(  '--binddn', 
				action='store', 
				metavar='dn',
				help='Distinguist name of bind user. A password will be requested unless argument --password is used.)')
	
	args = vars(parser.parse_args())
	env = environment()
	
	env.LDAPSERVER = args['host']
	env.BINDDN = args['binddn']
	env.BASEDN = args['basedn']
	
	if env.LDAPSERVER == None:print "No ldapserver provided, bailing out!";exit(1)
	if env.BASEDN == None:print "No basedn provided, bailing out!";exit(1)
	if env.BINDDN == None:print "No binddn provided, bailing out!";exit(1)

	if args['password'] == "":
		print env.BINDDN
		env.LDAPPW = getpass.getpass()
	else:
		env.LDAPPW = args['password']
	
	
	if args['add']:
		if args['g'] == None:
			error = helper_add_user(args['u'][0],args['u'][1], env)
			if error != "OK":print error
		else:
			if len(args['g']) != 2:print "usage: -g groupname {primairy, secondairy}"
			elif args['g'][1] == choices[0] or args['g'][1] == choices[1]:
				error = helper_add_group(args['g'][0], args['g'][1], env)
				if error != "OK":print error
			else:
				print "usage: -g groupname {primairy, secondairy}"
	else:
                if args['g'] == None:
                        error = helper_del_user(args['u'][0],args['u'][1], env)
                	if error != "OK":print error
		else:
			if len(args['g']) != 1:print "usage: -g groupname"
                        else:
				error = helper_del_group(args['g'][0], env)
				if error != "OK":print error
	sys.exit(1)
