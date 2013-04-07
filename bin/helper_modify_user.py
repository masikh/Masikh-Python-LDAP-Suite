#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import argparse,base64,cups,curses,getpass,ldap,ldif,locale,random,re,sha,string,sys,time,datetime
import helper_apply_ldif as apply_ldif
from os import system
from random import sample, choice
from copy import deepcopy

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

def WriteForm(content,fname, env):
	timestamp = int(time.time())
	fname = "%s.user-add.%s.ps"%(timestamp,fname)
	try:    
		f = open("%s%s"%(env.ACCOUNTFORM,fname),'w')
		try:
			f.writelines(content)
		finally:
			f.close()
	except IOError:
		pass
	return fname

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

def printform(s, fname, env):
	pos = 0
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	# Get all printers, select one and print
	conn = cups.Connection()
	printers = conn.getPrinters()
	length = len(printers)
	mypad = curses.newpad(length + 9,76)
	if pos < 5:pad_pos = 0
	else:pad_pos = pos - 5 
	selection = None
	s.erase()
	s.box()
	s.addstr(2, 2, "Print account form", curses.color_pair(3))
	s.addstr(4, 2, "Queue", curses.color_pair(1))
	s.addstr(4, 22, "Location", curses.color_pair(1))
	s.hline(5, 1, curses.ACS_HLINE, 76)
	s.addstr(19,2,"[Usage: [ESC] quits, [arrows] select printer, [enter] use selected printer]",curses.color_pair(1))
	while True:
		s.refresh()
		i = 0
		for printer in sorted(printers.iterkeys()):
			extra1 = 20 - len(printer)
			extra2 = 56 - len(printers[printer]["printer-location"])
			if pos == i:
				mypad.addstr(i, 0, "%s%s"%(str(printer),extra1*" "), curses.color_pair(3))
				mypad.addstr(i, 20, "%s%s"%(printers[printer]["printer-location"],extra2*" "), curses.color_pair(3))
				selection = printer
			else:
				mypad.addstr(i, 0, "%s%s"%(str(printer),extra1*" "), curses.color_pair(2))
				mypad.addstr(i, 20, "%s%s"%(printers[printer]["printer-location"],extra2*" "), curses.color_pair(2))
			i += 1
		mypad.refresh(pad_pos, 0, 9, 3, 20, 76)
		x = s.getch()
		if x == 27 or x == 127:
			break
		if x == 258 and pos < length - 1:pos += 1
		if x == 259 and pos > 0:pos -= 1
		if x == ord('\n') and length > 0:
			if type(fname) == list:
				for filename in fname:
					conn.printFile(selection, "%s%s"%(env.ACCOUNTFORM,filename), "Account Form", {})
			else:
				conn.printFile(selection, fname, "Account Form", {})
			break
		s.erase()
		s.box() 
		s.addstr(2, 2, "Print account form", curses.color_pair(3))
		s.addstr(4, 2, "Queue", curses.color_pair(1))
		s.addstr(4, 22, "Location", curses.color_pair(1))
		s.hline(5, 1, curses.ACS_HLINE, 76)
		s.addstr(19,2,"[Usage: [ESC] quits, [arrows] select printer, [enter] use selected printer]",curses.color_pair(1))
		if pos - pad_pos > 11:pad_pos += 3
		if pos - pad_pos < 0:pad_pos -= 3

def helper_select_autofs(s, env):
	pos = 0
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
	# Get all exports:
	exports = env.user_exports()
	length = len(exports)
	mypad = curses.newpad(length + 9,76)
	if pos < 5:pad_pos = 0
	else:pad_pos = pos - 5 
	selection = None
	s.erase()
	s.box()
	s.addstr(2,2,"Select export for account",curses.color_pair(3))
	s.addstr(4,2,"HINT: Older exports (before 2013) are at the bottom!",curses.color_pair(2))
	s.hline(5, 1, curses.ACS_HLINE, 76)

	s.addstr(19,2,"[Usage: [ESC] quits, [arrows] choose selection, [enter] make selection]",curses.color_pair(1))
	while True:
		s.refresh()
		i = 0
		for export in exports:
			extra1 = 20 - len(exports[export][0])
			extra2 = 58 - len(exports[export][1])
			if pos == i:
				mypad.addstr(i, 0, "%s%s"%(str(exports[export][0]),extra1*" "), curses.color_pair(3))
				mypad.addstr(i, 17, "%s%s"%(str(exports[export][1]),extra2*" "), curses.color_pair(3))
				selection = exports[export][1]
			else:
				mypad.addstr(i, 0, "%s%s"%(str(exports[export][0]),extra1*" "), curses.color_pair(2))
				mypad.addstr(i, 17, "%s%s"%(str(exports[export][1]),extra2*" "), curses.color_pair(2))
			i += 1
		mypad.refresh(pad_pos, 0, 9, 3, 20, 76)
		x = s.getch()
		if x == 27 or x == 127:
			break
		if x == 258 and pos < length - 1:pos += 1
		if x == 259 and pos > 0:pos -= 1
		if x == ord('\n') and length > 0:
			return selection
		s.erase()
		s.box() 
		s.addstr(2,2,"Select export for account",curses.color_pair(3))
		s.addstr(4,2,"HINT: Older exports (before 2013) are at the bottom!",curses.color_pair(2))
		s.hline(5, 1, curses.ACS_HLINE, 76)
		s.addstr(19,2,"[Usage: [ESC] quits, [arrows] choose export, [enter] make selection]",curses.color_pair(1))
		if pos - pad_pos > 11:pad_pos += 3
		if pos - pad_pos < 0:pad_pos -= 3
	return selection 

def helper_create_account_form(modified, clearpassword, env):
	error, content = openfile("./templateform.ps")
	DDMMJJJX = str(datetime.date.today())
	DDMMJJJY = str((datetime.date.today() + datetime.timedelta(6*365/12)).isoformat())
	content = re.sub("USERID" , modified['uid'][0], content)
	content = re.sub("employeeType" , modified['employeeType'][0], content)
	content = re.sub("GECOS" , str(modified['gecos'][0]), content)
	content = re.sub("employeeNumber" , modified['employeeNumber'][0], content)
	content = re.sub("COMPUTERACCOUNT" , modified['employeeType'][0], content)
	content = re.sub("DDMMJJJX" , DDMMJJJX, content)
	content = re.sub("DDMMJJJY" , DDMMJJJY, content)
	content = re.sub("PASSWORD" , clearpassword, content)
	fname = WriteForm(content, modified['uid'][0], env)
	return error, fname

def query_user(UID,env):
        DN="%s,%s"%(env.PEOPLE,env.BASEDN)
        FILTER="(&(objectClass=posixAccount)(uid=%s))"%(UID)
        ATTR=[  "sn",
                "loginShell", 
                "employeeType",
                "employeeNumber",
                "uidnumber",
                "gidnumber",
                "uid",
                "gecos",
                "cn",
                "homeDirectory",
                "objectClass",
		"userPassword"
             ]
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	ldap.set_option(*options[0])
	connection = ldap.initialize(env.LDAPSERVER)
        connection.simple_bind_s()
        try:result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
        if result == []:result = [("No such user!",{"": ""})]
        connection.unbind()
        return result

def getOldPassword(UID, env):
	error = "OK"
        DN="%s,%s"%(env.PEOPLE,env.BASEDN)
	FILTER="(&(objectClass=posixAccount)(uid=%s))" % UID
	ATTR=[ "userPassword" ]
	try:
		options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
	        connection.simple_bind_s(env.BINDDN, env.LDAPPW)
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:return error,""
	for dn, entry in result:
		return error, entry['userPassword'][0]

def isUser(UID, env):
        error="OK"
        DN="%s,%s"%(env.PEOPLE,env.BASEDN)
        FILTER="(&(objectClass=posixAccount)(uid=%s))"%UID
        ATTR = [ "uid" ]
        try:
		options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
                connection.simple_bind_s()
                result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, error:return "Generic error occured (are you logged in?)", True
	if result == []:return error, False
        else:return error,True

def get_Groups(UID, env):
	error = "OK"
	DN="%s,%s"%(env.GROUP,env.BASEDN)
        FILTER="(&(objectClass=posixGroup)(memberUid=" + UID + "))"
        ATTR = None
        try:
		options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, e:result = [("Generic error occured (are you logged in?)",{"": ""})]
        connection.unbind()	
	return error, result

def get_Netgroups(UID, env):
        error = "OK"
	DN="%s,%s"%(env.NETGROUP,env.BASEDN)
        FILTER="(&(objectClass=nisNetgroup)(nisNetgroupTriple=*," + UID + ",*))"
        ATTR=[ "nisNetgroupTriple" ]
	try:
		options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
	        connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_ONELEVEL, str(FILTER), ATTR)
        except ldap.LDAPError, error:return "Generic error occured (are you logged in?)",""
        connection.unbind()
        if result == []:return "No such user!",""
        return error,result

def get_Autofs(UID, env):
	error = "OK"
        DN="%s,%s"%(env.AUTOFS_HOME,env.BASEDN)
        FILTER="(&(objectClass=automount)(cn=" + UID + "))"
        ATTR=["automountInformation"]
	try:
		options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
	        connection.simple_bind_s()
        	result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
        except ldap.LDAPError, error:return "Generic error occured (are you logged in?)",""
        if result == []:return "No such user!",""
        connection.unbind()
        return error, result

def helper_next_free(TYPE, env):
	error = "OK"
	toprange = highest = 0
        DN="%s,%s"%(env.PEOPLE,env.BASEDN)
	FILTER="(uid=*)"
	ATTR=["uidNumber"]
	try:
		ranges = env.user_ranges()
		begin = ranges[TYPE][1]
		end= ranges[TYPE][2]
	except:begin=end=100
	try:
		options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
 		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, error: return "Generic error occured (are you logged in?)", toprange 
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

def helper_uid_isfree(uid, env):
	error = "OK"
        DN="%s,%s"%(env.PEOPLE,env.BASEDN)
	FILTER="(uid=*)"
	ATTR=["uidNumber"]
	try:
		options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
        	connection.simple_bind_s()
 		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
	except ldap.LDAPError, error: return "Generic error occured (are you logged in?)", false 
	connection.unbind()
	for dn, entry in result:
		if uid == entry[ATTR[0]][0]:
			return error, False
	return error, True

def del_user(UID, groups, netgroups, autofs, env):
	dofile = "dn: cn=%s,%s,%s\n" %(UID,env.AUTOFS_HOME,env.BASEDN)
	dofile += "changetype: delete\n\n"
	for dn,entry in groups:
		dofile += "dn: %s\n" % dn
		dofile += "changetype: modify\n"
		dofile += "delete: memberUid\n"
		for memberUid in entry['memberUid']:
			dofile += "memberUid: %s\n" % (memberUid)
		dofile += "\n"
	for dn,entry in netgroups:
		dofile += "dn: %s\n" % dn
		dofile += "changetype: modify\n"
                dofile += "delete: nisNetgroupTriple\n"
		for nisNetgroupTriple in entry['nisNetgroupTriple']:
			if re.match( '((.*),' + UID + ',(.*))', (nisNetgroupTriple), re.M|re.I):
				dofile += "nisNetgroupTriple: %s\n" % (nisNetgroupTriple)
		dofile += "\n"
	dofile += "dn: uid=%s,%s,%s\n" % (UID,env.PEOPLE,env.BASEDN)
	dofile += "changetype: delete\n\n"
	result = query_user(UID, env)
	error, oldpassword = getOldPassword(UID, env)
	undofile = ""
	for dn, entries in result:
                undofile += "dn: " + dn + "\n"
                for entry,value in dict.items(entries):
                        for multivalue in value:
                                undofile += "%s: %s\n" % (entry,multivalue)
	undofile += "userPassword: %s\n"%(oldpassword)
	undofile += "\n"
        for dn,entry in groups:
		undofile += "dn: %s\n" % dn
		undofile += "changetype: modify\n"
		undofile += "add: memberUid\n"
        	for memberUid in entry['memberUid']:
			if re.match(UID, (memberUid), re.M|re.I):
				undofile += "memberUid: %s\n" % (memberUid)
        	undofile += "\n"
        for dn,entry in netgroups:
                undofile += "dn: %s\n" % dn
                undofile += "changetype: modify\n"
                undofile += "add: nisNetgroupTriple\n"
                for nisNetgroupTriple in entry['nisNetgroupTriple']:
                        if re.match( '((.*),' + UID + ',(.*))', (nisNetgroupTriple), re.M|re.I):
                                undofile += "nisNetgroupTriple: %s\n" % (nisNetgroupTriple)
                undofile += "\n"
	for dn,entry in autofs:
		undofile += "dn: %s\n" % dn
		undofile += "cn: %s\n" % UID
		undofile += "objectClass: top\n"
		undofile += "objectClass: automount\n"
		undofile += "automountInformation: %s\n" % entry['automountInformation'][0]
	undofile += "\n"
	return dofile, undofile
	
def mod_user(modified, UID, groups, netgroups, autofs, env):
	dofile = "dn: cn=%s,%s,%s\n" %(UID,env.AUTOFS_HOME,env.BASEDN)
	dofile += "changetype: moddn\n"
	dofile += "newrdn: cn=%s\n"%(modified['uid'][0])
	dofile += "deloldrdn: 1\n\n"
	undofile = "dn: cn=%s,%s,%s\n" %(modified['uid'][0],env.AUTOFS_HOME,env.BASEDN)
	undofile += "changetype: moddn\n"
	undofile += "newrdn: cn=%s\n"%(UID)
	undofile += "deloldrdn: 1\n\n"
	for dn,entry in groups:
		dofile += "dn: %s\n" % dn
		dofile += "changetype: modify\n"
		dofile += "delete: memberUid\n"
		dofile += "memberUid: %s\n"%(UID)
		dofile += "-\n"
		dofile += "add: memberUid\n"
		dofile += "memberUid: %s\n\n"%(modified['uid'][0])
		undofile += "dn: %s\n" % dn
		undofile += "changetype: modify\n"
		undofile += "delete: memberUid\n"
		undofile += "memberUid: %s\n"%(modified['uid'][0])
		undofile += "-\n"
		undofile += "add: memberUid\n"
		undofile += "memberUid: %s\n\n"%(UID)
	for dn,entry in netgroups:
		dofile += "dn: %s\n" % dn
		dofile += "changetype: modify\n"
                dofile += "delete: nisNetgroupTriple\n"
		dofile += "nisNetgroupTriple: (-,%s,)\n"%(UID)
		dofile += "-\n"
		dofile += "add: nisNetgroupTriple\n"
		dofile += "nisNetgroupTriple: (-,%s,)\n\n"%(modified['uid'][0])
		undofile += "dn: %s\n" % dn
		undofile += "changetype: modify\n"
                undofile += "delete: nisNetgroupTriple\n"
		undofile += "nisNetgroupTriple: (-,%s,)\n"%(modified['uid'][0])
		undofile += "-\n"
		undofile += "add: nisNetgroupTriple\n"
		undofile += "nisNetgroupTriple: (-,%s,)\n\n"%(UID)
	return dofile, undofile
	
def helper_add_user(UID, s, env):
	error = "OK"
	# Check if user allready exits!
	error, isuser = isUser(UID, env)
	if error != "OK":return error
	if isuser == True:error = "ERROR: User %s already exists!" % UID;return error
	
	# User does not exits. Let's build one!
	letters = string.ascii_letters + string.digits + "%^-_+~.,\|="
	length = 10 
	newpassword = ''.join([random.choice(letters) for _ in range(length)])
	clearpassword = "%s"%str(newpassword)
	sha1 = base64.encodestring(sha.new(str(newpassword)).digest())
	newpassword = "{SHA}%s" % sha1
	types = env.user_ranges()
	lowest = 1000000000
	Type = ""
	for group in types.keys(): 
		if int(types[group][0]) < lowest:
			Type = group
			lowest = int(types[group][0])
	error, nextfree = helper_next_free(Type, env)
	
	init = modified = {}
	init["sn"]		= ["---"]
	init["loginShell"] 	= ["/bin/tcsh"]
	init["employeeType"] 	= ["%s" % str(Type)]
	init["employeeNumber"] 	= ["%s.%s" % (types[Type][0], str(nextfree))]
	init["uidNumber"] 	= ["%s" % str(nextfree)]
	init["gidNumber"] 	= ["%s" % types[Type][0]]
	init["uid"] 		= [UID]
	init["gecos"] 		= ["---"]
	init["cn"] 		= ["---"]
	init["homeDirectory"] 	= ["/home/%s" % UID]
	init["objectClass"] 	= [ "inetOrgPerson", "posixAccount", "shadowAccount" ]
	init["automountInformation"] = ['---']
	modified = deepcopy(init)
	init, modified = helper_add_userattr(s, env, init, modified)
	modified["userPassword"] = ["%s" % str(newpassword)]
	s.clear()
	s.box()
	s.addstr(2, 2, "Add user", curses.color_pair(3))
	error, isuser = isUser(modified['uid'][0], env)
	if isuser == True:error = "ERROR: User %s already exists!"%(modified['uid'][0]);return error
	i = 4
	warning = False
	for key in modified:
		if modified[key][0] == "---":
			warning = True
			s.addstr(i, 2, "WARNING: Attribute '%s' is not set."%(key),curses.color_pair(2))
			i += 1
	if warning:i+=1
	s.addstr(i, 2, "Do you wish to add user '%s' [y|n]"%(modified['uid'][0]),curses.color_pair(1))
	commit = getInput(s, i, 50, 1, 0, False)
	s.clear()
	s.box()
	s.addstr(2, 2, "Add user", curses.color_pair(3))
	if commit == 'y' or commit == 'Y':
		autofs = modified['automountInformation'][0]
		uid = modified['uid'][0]
		# Write account form to file
		error, fname = helper_create_account_form(modified, clearpassword, env)
		dofile = "dn: uid=%s,%s,%s\n"%(uid,env.PEOPLE,env.BASEDN)
		dofile += "objectClass: inetOrgPerson\n"
		dofile += "objectClass: posixAccount\n"
		dofile += "objectClass: shadowAccount\n"
		dofile += "sn: %s\n"%(modified['sn'][0])
		dofile += "userPassword: %s"%(modified['userPassword'][0])
		dofile += "loginShell: %s\n"%(modified['loginShell'][0])
		dofile += "employeeNumber: %s\n"%(modified['employeeNumber'][0])
		dofile += "employeeType: %s\n"%(modified['employeeType'][0])
		dofile += "uidNumber: %s\n"%(modified['uidNumber'][0])
		dofile += "gidNumber: %s\n"%(modified['gidNumber'][0])
		dofile += "uid: %s\n"%(modified['uid'][0])
		dofile += "gecos: %s\n"%(modified['gecos'][0])
		dofile += "cn: %s\n"%(modified['cn'][0])
		dofile += "homeDirectory: %s\n\n"%(modified['homeDirectory'][0])
		dofile += "dn: cn=%s,%s,%s\n"%(uid,env.AUTOFS_HOME,env.BASEDN)
		dofile += "objectClass: top\n"
		dofile += "objectClass: automount\n"
		dofile += "cn: %s\n"%(uid)
		dofile += "automountInformation: %s\n\n"%(autofs)
		undofile = "dn: uid=%s,%s,%s\n"%(uid,env.PEOPLE,env.BASEDN)
		undofile += "changetype: delete\n\n"
		undofile += "dn: cn=%s,%s,%s\n"%(uid,env.AUTOFS_HOME,env.BASEDN)
		undofile += "changetype: delete\n\n"
		content,error=apply_ldif.ldif2dict(dofile)
		if error != "OK":return error
		error=apply_ldif.apply_ldif(content,env)
		WriteLog(dofile, "add_user.done.%s"%(UID), env)
		WriteLog(undofile, "add_user.undo.%s"%(UID), env)
		s.addstr(4, 2, "User '%s' added succesfully!"%(uid), curses.color_pair(2))
		s.addstr(6, 2, "Login:    %s"%(uid), curses.color_pair(2))
		s.addstr(7, 2, "Password: %s"%clearpassword, curses.color_pair(2))
		s.addstr(9, 2, "Account form has been saved as: %s"%fname, curses.color_pair(2))
		s.addstr(11, 2, "Do you wish to print %s? [y|n]"%fname, curses.color_pair(1))
		toprinter = getInput(s, i, 50, 1, 0, False)
		if toprinter == 'y' or toprinter == 'Y':
			printform(s, "%s/%s"%(env.ACCOUNTFORM,fname), env)
		return error
	return error

def helper_del_user(UID, env):
	error = "OK"
	error, isuser = isUser(UID, env)
	if error != "OK":return error
	if isuser == False:return "No such user!"
	error, groups = get_Groups(UID, env)
	error, netgroups = get_Netgroups(UID, env)
	error, autofs = get_Autofs(UID, env)
	dofile, undofile = del_user(UID, groups, netgroups, autofs, env)
	content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":return error
        error=apply_ldif.apply_ldif(content,env)
	WriteLog(dofile, "delete_user.done.%s"%(UID), env)
	WriteLog(undofile, "delete_user.undo.%s"%(UID), env)
	return error 

def helper_change_password(UID, env):
	error = "OK"
	error,isuser = isUser(UID, env)
	if error != "OK":return error, ""
	if isuser == False:return "No such user!",""
	error,oldpassword = getOldPassword(UID, env)
	if error != "OK":return error,""
	letters = string.ascii_letters + string.digits + "%^-_+~.,\|="
	length = 10
	newpassword = ''.join([random.choice(letters) for _ in range(length)])
	sha1 = base64.encodestring(sha.new(str(newpassword)).digest())
	dofile = "dn: uid=%s,%s,%s\n" % (UID,env.PEOPLE,env.BASEDN)
	dofile += "changetype: modify\n"
	dofile += "replace: userPassword\n"
	dofile += "userPassword: {SHA}%s\n" % (sha1)
	undofile = "dn: uid=%s,%s,%s\n" % (UID,env.PEOPLE,env.BASEDN)
	undofile += "changetype: modify\n"
	undofile += "replace: userPassword\n"
	undofile += "userPassword: %s\n" % (oldpassword)
	content,error=apply_ldif.ldif2dict(dofile)
        if error != "OK":return error
        error=apply_ldif.apply_ldif(content,env)
	if error != "OK":return error
	WriteLog(dofile, "password_change.done.%s"%(UID), env)
	WriteLog(undofile, "password_change.undo.%s"%(UID), env)
	return error,newpassword

def helper_get_userattr(UID, env):
	error = "OK"
	# If netgroup does not exist; error message, return                             
	DN="%s,%s"%(env.PEOPLE,env.BASEDN)
	FILTER="(&(objectClass=posixAccount)(uid=%s))"%(UID)
	ATTR=None
	options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
	try:
		ldap.set_option(*options[0])
		connection = ldap.initialize(env.LDAPSERVER)
		connection.simple_bind_s()
		result = connection.search_s(DN, ldap.SCOPE_SUBTREE, FILTER, ATTR)
		connection.unbind()
	except ldap.LDAPError, e:return "Generic error occured (are you logged in?)", ""
	if result == []:
		error="ERROR: User %s does not exists!"%(UID)
		return error, result
	return error, result[0][1]

def select_employeeType(s, env, employeeType):
	types = env.user_ranges()
	selection = ""
	width = 0
	length = len(types) + 2
	for item in types.keys():
		if len(item) > width:width = len(item)
	width += 4
	s.hline(19, 2, curses.ACS_HLINE, 74)
	s.addstr(19,2,"[Use [arrows] to navigate and [enter] to select.]", curses.color_pair(1))
	screen = s.subwin(length, width, 7, 25)
	screen.erase()
	screen.box()
	pos = -1 
	while True:
		i=1
		if pos == -1:
			for item in types:
				if item == employeeType:
					pos = i
				i+=1
		i=1
		for item in types:
			if pos == i:
				selection = item
				screen.addstr(i,1," %s"%(item), curses.color_pair(3))
				extra = " " * (width - 3 - len(item))
				screen.addstr(i,2+len(item),extra, curses.color_pair(3))
			else:
				screen.addstr(i,1," %s"%(item), curses.color_pair(2))
				extra = " " * (width - 3 - len(item))
				screen.addstr(i,2+len(item),extra, curses.color_pair(2))
			i += 1
		screen.refresh()
		x = s.getch()
        	# down arrow 
        	if x == 258:
        	        if pos < len(types):pos += 1
        	        else:pos = 1
        	        x = ""
        	# up arrow 
        	elif x == 259:
        	        if pos > 1:pos -= 1
        	        else:pos = len(types)
        	        x = ""
        	elif x == ord('\n'):
        	        return selection

def helper_edit_userattr(s, env, pos, result, modified, selection):
	error = "OK"
	ranges = env.user_ranges()
	s.addstr(18, 2, " "*52, curses.color_pair(1))
	s.addstr(pos + 4, 24, " "*52, curses.color_pair(1))
	s.addstr(pos + 4, 24, "", curses.color_pair(1))
	if selection == "employeeType":
		temp = select_employeeType(s,env, modified['employeeType'][0])
		modified[selection][0] = temp
		modified['gidNumber'][0] = ranges[temp][0]
		if 'uidNumber' in modified:
			error, nextfree = helper_next_free(temp, env)
			modified['uidNumber'][0] = str(nextfree)
			modified['employeeNumber'][0] = "%s.%s"%(modified['gidNumber'][0],modified['uidNumber'][0])
	elif selection == "uid":
		temp = modified[selection][0]
		modified[selection][0] = getInput(s, pos + 4, 24, 52, 6, True)
		if modified[selection][0] == "":modified[selection][0] = temp
	elif selection == "loginShell":
		temp = modified[selection][0]
		modified[selection][0] = getInput(s, pos + 4, 24, 52, 5, True)
		if modified[selection][0] == "":modified[selection][0] = temp
	elif selection == "gidNumber" and 'uidNumber' in modified:
		temp = modified[selection][0]
		modified[selection][0] = getInput(s, pos + 4, 24, 52, 6, True)
		if modified[selection][0] == "":modified[selection][0] = temp
	elif selection == "gecos":
		temp = modified[selection][0]
		modified[selection][0] = getInput(s, pos + 4, 24, 52, 4, True)
		if modified[selection][0] == "":modified[selection][0] = temp
	elif selection == "sn":
		temp = modified[selection][0]
		modified[selection][0] = getInput(s, pos + 4, 24, 52, 4, True)
		if modified[selection][0] == "":modified[selection][0] = temp
	elif selection == "homeDirectory":
		temp = modified[selection][0]
		modified[selection][0] = getInput(s, pos + 4, 24, 52, 5, True)
		if modified[selection][0] == "":modified[selection][0] = temp
	elif selection == "cn":
		temp = modified[selection][0]
		modified[selection][0] = getInput(s, pos + 4, 24, 52, 4, True)
		if modified[selection][0] == "":modified[selection][0] = temp
	elif selection == "employeeNumber":
		temp = modified[selection][0]
		modified[selection][0] = getInput(s, pos + 4, 24, 52, 3, True)
		if modified[selection][0] == "":modified[selection][0] = temp
	elif selection == "automountInformation":
		modified[selection][0] = helper_select_autofs(s, env)	
	else:
		error = "[attribute '%s' is not modifiable]"%(selection)
		return error, modified
	return error, modified

def helper_modify_userattr_nav(s, env, x, pos, result, modified, selection):
	error = "OK"
	escape = False
	# if ESC pressed
	if x == 27:escape = True
	# down arrow 
        if x == 258:
                if pos < len(modified) - 1:pos += 1
		else:pos = 0
                x = ""
        # up arrow 
        elif x == 259:
                if pos > 0:pos -= 1
                else:pos = len(modified) - 1 
                x = ""
	elif x == ord('\n'):
		error, modified = helper_edit_userattr(s, env, pos, result, modified, selection)
	return error, escape, x, pos, modified

def helper_modified_user_to_ldif(env, result, modified):
	dofile = ""; undofile = ""; temp1 = ""; temp2 = ""; autofs_orig = ""; autofs2_new = "";	error = ""

	autofs_orig = result['automountInformation'][0]
	autofs_new = modified['automountInformation'][0]
	del result['automountInformation']
	del modified['automountInformation']
	if result['uid'] != modified['uid']:
		dofile += "dn: uid=%s,%s,%s\n"%(result['uid'][0],env.PEOPLE,env.BASEDN)
		dofile += "changetype: moddn\n"
		dofile += "newrdn: uid=%s\n"%(modified['uid'][0]) 
		dofile += "deleteoldrdn: 1\n\n"
		undofile += "dn: uid=%s,%s,%s\n"%(modified['uid'][0],env.PEOPLE,env.BASEDN)
		undofile += "changetype: moddn\n"
		undofile += "newrdn: uid=%s\n"%(result['uid'][0]) 
		undofile += "deleteoldrdn: 1\n\n"
		UID = result['uid'][0]
		error, groups = get_Groups(UID, env)
		error, netgroups = get_Netgroups(UID, env)
		error, autofs = get_Autofs(UID, env)
		temp1, temp2 = mod_user(modified, UID, groups, netgroups, autofs, env)
		dofile += temp1
		undofile += temp2	
	for item in result:
		# Make sure uid change is skipped!
		if item == "uid":continue
		else:
			if result[item] != modified[item]:
				dofile += "dn: uid=%s,%s,%s\n"%(modified['uid'][0],env.PEOPLE,env.BASEDN)
				dofile += "changetype: modify\n"
				dofile += "replace: %s\n"%(item)
				dofile += "%s: %s\n\n"%(item, modified[item][0])
				undofile += "dn: uid=%s,%s,%s\n"%(result['uid'][0],env.PEOPLE,env.BASEDN)
				undofile += "changetype: modify\n"
				undofile += "replace: %s\n"%(item)
				undofile += "%s: %s\n\n"%(item, result[item][0])
	if autofs_new != "":
		dofile += "dn: cn=%s,%s,%s\n"%(modified['uid'][0],env.AUTOFS_HOME,env.BASEDN)
		dofile += "changetype: modify\n"
		dofile += "replace: automountInformation\n"
		dofile += "automountInformation: %s\n\n"%(autofs_new)
		undofile += "dn: cn=%s,%s,%s\n"%(result['uid'][0],env.AUTOFS_HOME,env.BASEDN)
		undofile += "changetype: modify\n"
		undofile += "replace: automountInformation\n"
		undofile += "automountInformation: %s\n\n"%(autofs_orig)
	return dofile, undofile, error

def helper_add_userattr(s, env, result, modified):
	error = "OK"
	pos = 0
	escape = False
	if result['objectClass']:
		del result['objectClass']
		del modified['objectClass']
	changed = False
	while not escape:
		s.erase()
		s.box()
		s.addstr(2, 2, "Add user", curses.color_pair(3))
		selection = ""
		# RESET attributes if attr 'employeeType' is switched back to original setting.
		# Modificatations take place in helper_modify_userattr_nav()
		if changed and modified['employeeType'] == result['employeeType']:
			modified['uidNumber'] = result['uidNumber']
			modified['gidNumber'] = result['gidNumber']
			modified['employeeNumber'] = result['employeeNumber']
			changed = False
		i=4
		if error != "OK":s.addstr(19, 2, error, curses.color_pair(1))
		else:s.addstr(19, 2, "[Press [ESC] when done, [arrow keys] to select and [enter] to edit.]", curses.color_pair(1))
		for attr in modified:
			if pos + 4 == i:
				s.addstr(i, 2,"%s:"%(attr), curses.color_pair(2))
				if result[attr][0] != modified[attr][0]:
					s.addstr(i, 1, "*", curses.color_pair(1))
				else:
					s.addstr(i, 1, " ", curses.color_pair(1))
				s.addstr(i, 24, modified[attr][0], curses.color_pair(1))
				selection = attr
			else:
				s.addstr(i, 2,"%s:"%(attr), curses.color_pair(2))
				if result[attr][0] != modified[attr][0]:
					s.addstr(i, 1, "*", curses.color_pair(1))
				else:
					s.addstr(i, 1, " ", curses.color_pair(1))
				s.addstr(i, 24, modified[attr][0], curses.color_pair(2))
			i += 1
		x = s.getch()
		error, escape, x, pos, modified = helper_modify_userattr_nav(s, env, x, pos, result, modified, selection)
		if modified['employeeType'] != result['employeeType']:changed = True
		# STOP LOOP
		if escape:break
	s.hline(19, 2, curses.ACS_HLINE, 75)
	return result, modified

def helper_modify_userattr(s, env, result, modified):
	error = "OK"
	pos = 0
	escape = False
	if result['objectClass']:
		del result['objectClass']
		del modified['objectClass']
	changed = False
	while not escape:
		s.erase()
		s.box()
		if 'uidNumber' in modified:
			s.addstr(2, 2, "Modify user attributes", curses.color_pair(3))
		else:
			s.addstr(2, 2, "Add users", curses.color_pair(3))
		selection = ""
		# RESET attributes if attr 'employeeType' is switched back to original setting.
		# Modificatations take place in helper_modify_userattr_nav()
		if changed and modified['employeeType'][0] == result['employeeType'][0]:
			modified['uidNumber'][0] = result['uidNumber'][0]
			modified['gidNumber'][0] = result['gidNumber'][0]
			modified['employeeNumber'][0] = result['employeeNumber'][0]
			changed = False
		i=4
		if error != "OK":s.addstr(19, 2, error, curses.color_pair(1))
		else:s.addstr(19, 2, "[Press [ESC] when done, [arrow keys] to select and [enter] to edit.]", curses.color_pair(1))
		for attr in modified:
			if 'uidNumber' not in modified and attr == 'gidNumber':
				continue
			elif pos + 4 == i:
				s.addstr(i, 2,"%s:"%(attr), curses.color_pair(2))
				if result[attr][0] != modified[attr][0]:
					s.addstr(i, 1, "*", curses.color_pair(1))
				else:
					s.addstr(i, 1, " ", curses.color_pair(1))
				s.addstr(i, 24, modified[attr][0], curses.color_pair(1))
				selection = attr
			else:
				s.addstr(i, 2,"%s:"%(attr), curses.color_pair(2))
				if result[attr][0] != modified[attr][0]:
					s.addstr(i, 1, "*", curses.color_pair(1))
				else:
					s.addstr(i, 1, " ", curses.color_pair(1))
				s.addstr(i, 24, modified[attr][0], curses.color_pair(2))
			i += 1
		x = s.getch()
		error, escape, x, pos, modified = helper_modify_userattr_nav(s, env, x, pos, result, modified, selection)
		if modified['employeeType'][0] != result['employeeType'][0]:changed = True 
		# STOP LOOP
		if escape:break
	s.hline(19, 2, curses.ACS_HLINE, 75)
	return result, modified

def getInput(screen,offset_y,offset_x,length,alfabet,cursor):
	allowed = {     0 : (set("y" + "Y" + "n" + "N"),
                            "Use yY/nN only!"),
                        1 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+"),
                            "Use -_.+ a-z A-Z 0-9 only"),
                        2 : (set(string.digits + string.ascii_letters + "-" + "_" + "." + "+" + "=" + ","),
                            "Use -_.+=, a-z A-Z 0-9 only"),
                        3 : (set(string.digits + "."),
                            "Use 0-9 . only"),
                        4 : (set(string.digits + string.ascii_letters + string.punctuation + " " + "-" + "_" + "." + "+" + "=" + "," + "Á" + "á" + "Ấ" + "ấ" + "Ắ" + "ắ" + "Ǻ" + "ǻ" + "Ǽ" + "ǽ" + "Ć" + "ć" + "Ḉ"     + "ḉ" + "É" + "é" + "Ế" + "ế" + "Ḗ" + "ḗ" + "Ǵ" + "ǵ" + "Í" + "í" + "Ḯ" + "ḯ    " + "Ḱ" + "ḱ" + "Ĺ" + "ĺ" + "Ḿ" + "ḿ" + "Ń" + "ń" + "Ó" + "ó" + "Ố" + "ố" +     "Ṍ" + "ṍ" + "Ṓ" + "ṓ" + "Ǿ" + "ǿ" + "Ṕ" + "ṕ" + "Ŕ" + "ŕ" + "Ś" + "ś" + "Ṥ"     + "ṥ" + "Ú" + "ú" + "Ǘ" + "ǘ" + "Ứ" + "ứ" + "Ṹ" + "ṹ" + "Ẃ" + "ẃ" + "Ý" + "ý    " + "Ź" + "ź" + "Ѓ" + "ѓ" + "Ќ" + "ќ"),
                            "Use -_.+=, 'space/accents' a-z A-Z 0-9 only"),
                        5 : (set(string.digits + string.ascii_letters + "/" + "-" + "_" + "." + "+"),
                            "Use -_.+ a-z A-Z 0-9 only"),
                        6 : (set(string.digits + string.ascii_lowercase + "-" + "_" + "." + "+"),
                            "Use -_.+ a-z 0-9 only"),
                        7 : (set(string.digits),
                            "Use 0-9 only"),
                        8 : (set(string.digits + string.ascii_letters + string.punctuation + " " + ":" + "-" + "_" + "." + "+" + "=" + "," + "Á" + "á" + "Ấ" + "ấ" + "Ắ" + "ắ" + "Ǻ" + "ǻ" + "Ǽ" + "ǽ" + "Ć" + "ć" + "Ḉ"     + "ḉ" + "É" + "é" + "Ế" + "ế" + "Ḗ" + "ḗ" + "Ǵ" + "ǵ" + "Í" + "í" + "Ḯ" + "ḯ    " + "Ḱ" + "ḱ" + "Ĺ" + "ĺ" + "Ḿ" + "ḿ" + "Ń" + "ń" + "Ó" + "ó" + "Ố" + "ố" +     "Ṍ" + "ṍ" + "Ṓ" + "ṓ" + "Ǿ" + "ǿ" + "Ṕ" + "ṕ" + "Ŕ" + "ŕ" + "Ś" + "ś" + "Ṥ"     + "ṥ" + "Ú" + "ú" + "Ǘ" + "ǘ" + "Ứ" + "ứ" + "Ṹ" + "ṹ" + "Ẃ" + "ẃ" + "Ý" + "ý    " + "Ź" + "ź" + "Ѓ" + "ѓ" + "Ќ" + "ќ"),
			    "Use -_.+=,: 'space/accents' a-z A-Z 0-9 only")
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

                if x == ord('\n') and length != 1:break
                elif x == 27 and alfabet == 8:value = "ESCAPE";break
		elif x == 27 and length > 1:value = "";break
                elif x == 127 or x == 263:
                        value = value[:-1]
                        if i > 0:i -= 1
                        x = ""
                        screen.addstr(offset_y, offset_x, " " * (length))
                        screen.addstr(offset_y, offset_x, "%s"%(value))
                        continue
                elif string_x not in allowed[alfabet][0]:
                        screen.addstr(wy - 1, 2,"[Wrong input: %s]"%(allowed[alfabet][1]),curses.color_pair(1))
                        screen.addstr(offset_y, offset_x, " " * (length))
                        screen.addstr(offset_y, offset_x, "%s"%(value))
                        continue
                elif length == 1:
                        curses.curs_set(0)
                        curses.noecho()
                        value += string_x
                        return value
                elif i >= length:
                        screen.addstr(wy - 1, 2,"[No more than %s characters allowed]"%(length),curses.color_pair(    1))
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

def GUI_change_password(env,screen):
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Change password", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
        UID = getInput(s,4,18,56,1,True)
        if UID == "":
		s.erase()
		return
	error,newpassword = helper_change_password(UID, env)
	if error != "OK":s.addstr(6, 2, error, curses.color_pair(2))
	else:
		s.addstr(6, 2, "Password reset: %s" % error, curses.color_pair(2))
		s.addstr(7, 2, "New Password: %s" % newpassword, curses.color_pair(2))
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return

def GUI_modify_user(env, screen):
	makechanges = ""
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Modify user attributes", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
	UID = getInput(s,4,18,58,2,True)
	if UID == "":
		s.erase()
		return
	error, result = helper_get_userattr(UID, env)
	if error != "OK":
		s.addstr(4, 2, error, curses.color_pair(2))
		s.getch()
		return
	error, result1 = get_Autofs(UID, env)
	if error != "OK":
		s.addstr(4, 2, error, curses.color_pair(2))
		s.getch()
		return
	result['automountInformation'] = result1[0][1]['automountInformation']
	modified = deepcopy(result)
	s.erase()
	s.box()
	s.addstr(2, 2, "Modify user attributes", curses.color_pair(3))
	if error != "OK":
		s.addstr(4, 2, error, curses.color_pair(2))
		s.getch()
		return
	result, modified = helper_modify_userattr(s, env, result, modified)
	if result != modified:
		# Modifications have taken place:
		dofile, undofile, error = helper_modified_user_to_ldif(env, result, modified)
		# TO LDAPSERVER AND LOG
		s.addstr(16, 2, "Do you wish to commit the changes? [y|n]", curses.color_pair(1))
		makechanges = getInput(s, 15, 40, 1, 0, False)
		if makechanges == "y" or makechanges == "Y":
			s.addstr(16, 2, "%s"%env.LOGS, curses.color_pair(1))
			content,error=apply_ldif.ldif2dict(dofile)
			if error != "OK":return error
			error=apply_ldif.apply_ldif(content,env)
			WriteLog(dofile, "modify_user.done.%s"%(UID), env)
			WriteLog(undofile, "modify_user.undo.%s"%(UID), env)
			s.erase()
			s.box()
			s.addstr(2, 2, "Modify user attributes", curses.color_pair(3))
			if error == "OK":
				s.addstr(4, 2, "User %s modified."%(UID), curses.color_pair(2))
			else:
				s.addstr(6, 2, "%s"%(error), curses.color_pair(2))
			s.getch()
	s.erase()
	return

def GUI_add_user(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Add user", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter new username: ", curses.color_pair(1))
	UID = getInput(s,4, 22, 54, 6,True)
	if UID == "":
		s.erase()
		return
	error = helper_add_user(UID, s, env)
	if error != "OK":
		s.addstr(4, 2, error, curses.color_pair(2))
		s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
		s.getch()
	s.erase()
	return

# get userinput from a cut and paste facility
def pastebox(s):
	s.addstr(4, 2, "File format: studentnumber:firstname:initials:preposition:surname", curses.color_pair(2))
	s.addstr(6, 2, "e.g.: 1046853:Ran:R.::An", curses.color_pair(2))
	s.addstr(7, 2, "      1286781:Emmanuel:E.:A:Appiah", curses.color_pair(2))
	s.addstr(8, 2, "      1292285:Andrada:A.I.::Bacaoanu", curses.color_pair(2))
	s.addstr(9, 2, "      .", curses.color_pair(2))
	s.addstr(9, 10, "<- End of file marker!!!", curses.color_pair(2))
	s.addstr(11, 2, "Paste file contents here:", curses.color_pair(1))
	s.addstr(11, 28, "Maximal 500 lines, including the '.' marker!", curses.color_pair(2))
	line = input = ""
	i = 0
	pastebox = s.subwin(7, 76, 15, 2)
	pastebox.box()
	pastepad = curses.newpad(500,200)
	s.addstr(17, 2, "")
	s.refresh()
	discarded = 0
	while line != ".":
		line = ""
		i += 1
		line = getInput(s, 17, 2, 73, 8, True)
		s.addstr(19, 2, "[Use [ESC] to abort or '.' to mark end of input!]", curses.color_pair(1))
		if line == "ESCAPE":
			s.addstr(17, 2, " " * 74);s.addstr(17, 2, "")
			input = ""
			break
		if line == "." or line == "":
			i -= 1
			s.addstr(17, 2, "")
		else:
			count = 0
			for part in line.split(':'):
				count += 1
			if count == 5:
				input += "%s\n"%(line)
				pastepad.addstr(i+4, 0, "%s"%(line), curses.color_pair(2))
				pastepad.refresh(i+1, 0, 16, 3, 19, 76)
			else:
				discarded += 1
				i -= 1
			s.addstr(11, 28, " " * 45);s.addstr(11, 28, "%s lines pasted, %s lines discarded."%(i, discarded), curses.color_pair(2))
			s.addstr(17, 2, " " * 74);s.addstr(17, 2, "")
	return input, i

def build_users(user, env):
	dofile = undofile = ""
	netgroups = env.user_netgroups()
	for entry in user:
		dofile += "dn: cn=%s,%s,%s\n"%(user[entry]['uid'],env.AUTOFS_HOME,env.BASEDN)
		dofile += "cn: %s\n"%(user[entry]['cn'])
		dofile += "objectClass: top\n"
		dofile += "objectClass: automount\n"
		dofile += "automountInformation: %s\n\n"%(user[entry]['automountInformation'])
		
		undofile += "dn: cn=%s,%s,%s\n"%(user[entry]['uid'],env.AUTOFS_HOME,env.BASEDN)
		undofile += "changetype: delete\n\n"

		dofile += "dn: uid=%s,%s,%s\n"%(user[entry]['uid'],env.PEOPLE,env.BASEDN)
		dofile += "objectClass: inetOrgPerson\n"
		dofile += "objectClass: posixAccount\n"
		dofile += "objectClass: shadowAccount\n"
		
		undofile += "dn: uid=%s,%s,%s\n"%(user[entry]['uid'],env.PEOPLE,env.BASEDN)
		undofile += "changetype: delete\n\n"
	
		for value in user[entry]:
			if value != "automountInformation":
				dofile += "%s: %s\n"%(value, user[entry][value])
		dofile += "\n"

		for group in netgroups[user[entry]['employeeType']]:
			dofile += "dn: cn=%s,%s,%s\n"%(group,env.NETGROUP,env.BASEDN)
			dofile += "changetype: modify\n"
			dofile += "add: nisNetgroupTriple\n"
			dofile += "nisNetgroupTriple: (-,%s,)\n\n"%(user[entry]['uid'])
			
			undofile += "dn: cn=%s,%s,%s\n"%(group,env.NETGROUP,env.BASEDN)
			undofile += "changetype: modify\n"
			undofile += "delete: nisNetgroupTriple\n"
			undofile += "nisNetgroupTriple: (-,%s,)\n\n"%(user[entry]['uid'])

	return dofile, undofile

def add_users(input, modified, env, s):
	error = "OK"

	column_header = ['employeeNumber',
			 'cn',
			 'voorletters',
			 'tussenvoegsel',
			 'sn']
	user = {}
	isuser = True
	# Build list of users
	i = 0
	s.erase()
	for line in input.split('\n'):
		if line != "":
			entryDict = {}
			tempList = line.split(':')
			for j, header in enumerate(column_header):
				entryDict[header] = tempList[j].strip()
			user[i] = entryDict 
			i += 1
	i = 0
	# Keep a list of new free user names (they might be taken before added)
	# e.g. add multiple users with same name (follownummber)
	newusers = []
	userpassword = {}
	forms = []
	nextfree = fname = ""
	for i in user:
		# Build attributes from user
		user[i]['loginShell'] = "/bin/tcsh"
		user[i]['cn'] = user[i]['cn']
		user[i]['sn'] = user[i]['sn']
		user[i]['uid'] = "%s%s"%(user[i]['cn'][:1].lower(),user[i]['sn'][0:7].lower())
		user[i]['gidNumber'] = modified['gidNumber'][0]
		user[i]['automountInformation'] = modified['automountInformation'][0]
		user[i]['employeeType'] = modified['employeeType'][0]


		# Check if username is free, if not append number to name!
		k = 1
		uid = user[i]['uid']
		while isuser: 
			error, isuser = isUser(user[i]['uid'], env)
			if user[i]['uid'] in newusers:
				isuser = True 
			if isuser:
				user[i]['uid'] = "%s%s"%(uid, str(k))
				k += 1
		isuser = True 
		
		# Hold track of usernames not yet in LDAP (Now reserved names!)			
		newusers.insert(0, user[i]['uid'])
		result = True

		# Get next free UID numbers for given type of user
		if nextfree == "":
			error, newuid = helper_next_free(modified['employeeType'][0], env)
			nextfree = newuid
			if error != "OK": return error
			user[i]['uidNumber'] = newuid
		else:
			freeuid = False
			while not freeuid:
				nextfree += 1
				error, freeuid = helper_uid_isfree(nextfree, env)
			user[i]['uidNumber'] = nextfree


		# Build attributes from user 
		user[i]['homeDirectory'] = "/home/%s"%(user[i]['uid'])
		# Build gecos information
		if user[i]['voorletters'] == "":
			user[i]['gecos'] = "%s %s %s"%(user[i]['cn'],user[i]['tussenvoegsel'],user[i]['sn'])
		elif user[i]['tussenvoegsel'] == "":
			user[i]['gecos'] = "%s %s"%(user[i]['voorletters'],user[i]['sn'])
		else:
			user[i]['gecos'] = "%s %s %s"%(user[i]['voorletters'],user[i]['tussenvoegsel'],user[i]['sn'])
	
		# Make password
		letters = string.ascii_letters + string.digits + "%^-_+~.,\|="
		length = 10
		newpassword = ''.join([random.choice(letters) for _ in range(length)])
		clearpassword = "%s"%str(newpassword)
		sha1 = base64.encodestring(sha.new(str(newpassword)).digest()).rstrip()
		user[i]['userPassword'] = "{SHA}%s"%(sha1)
		userpassword[i] = { 'userPassword' : clearpassword }
		# Remove unwanted attributes
		del user[i]['voorletters']
		del user[i]['tussenvoegsel']
		i += 1
	# Build account form for current user. Save fname(s) in a list.
	for i in user:
		temp = user[i]
		error, fname = create_account_form(temp, userpassword[i]['userPassword'], env)
		forms += [fname]

	dofile, undofile = build_users(user, env)
	content, error = apply_ldif.ldif2dict(dofile)
	error = apply_ldif.apply_ldif(content, env)
	WriteLog(dofile, "multiple_user_add.done.%s"%(user[0]['employeeType']), env)
	WriteLog(undofile, "multiple_user_add.undo.%s"%(user[0]['employeeType']), env)
	return error, forms

def create_account_form(modified, clearpassword, env):
	error, content = openfile("./templateform.ps")
	DDMMJJJX = str(datetime.date.today())
	DDMMJJJY = str((datetime.date.today() + datetime.timedelta(6*365/12)).isoformat())
	content = re.sub("USERID"		, modified['uid'], content)
	content = re.sub("employeeType"		, modified['employeeType'], content)
	content = re.sub("GECOS"		, str(modified['gecos']), content)
	content = re.sub("employeeNumber"	, modified['employeeNumber'], content)
	content = re.sub("COMPUTERACCOUNT"	, modified['employeeType'], content)
	content = re.sub("DDMMJJJX"		, DDMMJJJX, content)
	content = re.sub("DDMMJJJY"		, DDMMJJJY, content)
	content = re.sub("PASSWORD"		, clearpassword, content)
	fname = WriteForm(content, modified['uid'], env)
	return error, fname


def GUI_multiple_add_user(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Add users", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	
	# Get input from user in a pastebox
	input, numusers = pastebox(s) 
	
	# Set user attributes
	result = {}
	modified = {}
	ranges = env.user_ranges()
	result['employeeType'] = ["Student"]
	result['gidNumber'] = [ranges['Student'][0]]
	if input != "":
		result['objectClass'] = ["---"]
		result['automountInformation'] = ["---"]
		modified = deepcopy(result)
		result, modified = helper_modify_userattr(s, env, result, modified)
		if modified['gidNumber'][0] == "---" or modified['automountInformation'] == ["---"]:
			s.addstr(7, 2, "User attributes can not be empty!", curses.color_pair(2))
			s.hline(19, 2, curses.ACS_HLINE, 74)
			s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
			s.getch()
			return
		else:
			s.addstr(7, 2, "Ready to add %s users, do you wish to continue? [y|n]"%(numusers), curses.color_pair(1))
			commit = getInput(s, 17, 2, 1, 0, False)
			# Bailout or not!
			if commit == 'n' or commit == 'N':
				return
			s.box()
			s.refresh()
			error, forms = add_users(input, modified, env, s)
			s.box()
			s.refresh()
			if error == "OK":
				s.addstr(2, 2, "Add users", curses.color_pair(3))
				s.addstr(4, 2, "%s Users added."%(numusers), curses.color_pair(2))
				s.addstr(6, 2, "Do you wish to print the account forms? [y|n]", curses.color_pair(1))
				#Bailout or not!
				commit = getInput(s, 17, 2, 1, 0, False)
				if commit == 'n' or commit == 'N':
					return
				else:
					printform(s, forms, env)	
	s.erase()
	return

def GUI_multiple_del_user(env, screen):
	return

def GUI_del_user(env, screen):
        s = curses.newwin(20, 78, 3, 1)
	s.erase()
	s.keypad(1)
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_WHITE)
        s.box()
	s.addstr(2, 2, "Delete user", curses.color_pair(3))
	s.addstr(19, 2, "[Use [ESC] to abort!]", curses.color_pair(1))
	s.addstr(4, 2, "Enter username: ", curses.color_pair(1))
	UID = getInput(s,4,18,58,1,True)
	if UID == "":
		s.erase()
		return
	error = helper_del_user(UID, env)
	s.addstr(6, 2, error, curses.color_pair(2))
	s.addstr(19, 2, "[Press any key to continue]", curses.color_pair(1))
	s.getch()
	s.erase()
	return

if __name__ == "__main__":
	sys.exit(1)
