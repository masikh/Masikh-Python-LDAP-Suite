#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

import argparse,base64,getpass,ldap,ldif,os,re,sys,time
import ldap.modlist as modlist
from collections import OrderedDict
#from environment import *
from string import lower

"""apply_ldif.py: Apply an LDIF file to an LDAP server."""
__author__ = "Robert Nagtegaal"
__copyright__ = "Copyright 2012, Masikh"
__credits__ = ["Kristian Rietveld", "Mattias Holm"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Robert Nagtegaal"
__email__ = "robert@masikh.org, masikh@gmail.com"
__status__ = "(BETA)"

class environment:
        LDAPSERVER=BASEDN=BINDDN=LDAPPW=""
	LDBUG = False
	VERBOSE = False

def unindent(LDIF):
	"""
	This function takes an ldif file and unindents it. Meaning that base64 encodeded strings are
	reconcaternated on one line. It returns the concaternated LDIF.
	"""
        output = ""
        for line in LDIF.split('\n'):
                indent = re.match('^\ (.*)', line)
                if indent:
                        output += line.lstrip()
                else:
                        if output !="":output += "\n" + line
                        else: output += line # Omit false \n at begin
        return output[:-1] # return and Omit false \n at the end

def unfold(LDIF):
	"""
	This function takes an ldif and unfolds it. Meaning all dash marks are relaced with
	their respective dn and modification type (unfolding). This makes it possible to parse
	each dn in the ldif as a seperate state.
	"""
	output = currentdn = ""
	UNFOLD = False
	for line in LDIF.split('\n'):
		dash = re.match( '^-$', line)
		match = re.match( '^dn: (.*)', line )
		if match:
			currentdn = match.group(1)
			output += "%s\n" % line
		elif dash:
			output += "\ndn: %s\n" % currentdn
			output += "changetype: modify\n"
		else:
			output += "%s\n" % line
	return output[:-1] # return and omit false \n at the end 

def ldif2dict(LDIF):
	"""
	This function builds an list of ordered dictionairies from an ldif file. The input (LDIF) is
	in the form of a flat ldif ascii file. Comments and white lines are allowed. This function
	returns	a list of dictionairies. Comments are discarded all other fields are included in the 
	dictionairy. 
	
	Dependencies: unident(LDIF) and unfold(LDIF). These resp. convert base64 to one line and gives
	the long version of a - notation.

	Example output:
	
	'cn=u-lab_3,ou=Netgroup,dc=unix,dc=example,dc=org': { 'nisNetgroupTriple': ['(-,jdoe,)'],
							      'changetype': ['modify'],
	       						      'delete': ['nisNetgroupTriple']},
	'cn=u-lab_4,ou=Netgroup,dc=unix,dc=example,dc=org': { 'nisNetgroupTriple': ['(-,jdoe,)'],
							      'changetype': ['modify'],
							      'delete': ['nisNetgroupTriple']}}
	"""
	
	LDIF = unindent(LDIF)
	LDIF = unfold(LDIF)
	dictionairy = OrderedDict()
        dictlist = []
	currentdn = ""
	error="OK"
	control_attribute = re.compile('^objectclass: (.*)|^changetype: (.*)|^add: (.*)|^delete: (.*)|^replace: (.*)',re.IGNORECASE)
	# for each line in LDIF file, do...
	for line in LDIF.split("\n"):
		# Test for ~valid~ input:
                match = re.match( '^(.*?): (.*)', line )
		comments = re.match( '^#(.*)|^$', line )
		encoded = re.match( '^(.*?):: (.*)', line )
		if control_attribute.match(line):
			line = line.lower()
			match = re.match( '^(.*?): (.*)', line )
		if encoded:
			line = encoded.group(1) + ": " + encoded.group(2)
			match = re.match( '^(.*?): (.*)', line )
		if comments:continue # discard comments and "\n"
		elif match:
                        # If begin of new DN container... 
               	        if match.group(1) == "dn":
				if currentdn != "":dictlist += [ (dictionairy) ]
				dictionairy = OrderedDict()	
               	                currentdn = match.group(2)
                                if not dictionairy.has_key( currentdn ):
                                        dictionairy[ currentdn  ] = OrderedDict()
			# else fill DN containers attributes...
                        else:
			        if not dictionairy[ currentdn ].has_key( match.group(1) ):
                                        dictionairy[ currentdn ][ match.group(1) ] = [ match.group(2) ]
                                else:
                                       if not match.group(2) in dictionairy[ currentdn ][ match.group(1) ]:
                                                dictionairy[ currentdn ][ match.group(1) ] += [ match.group(2) ]
        	else:
			error="Invalid LDIF File!"
	dictlist += [ (dictionairy) ]
	return dictlist,error

def apply_ldif(content,env):
	"""
	Receive an list of - ordered - dictionairies with ldif 
	content and apply content  on ldap server.  Modify, delete
	and other ldif command are stored in a state. Each 'DN' is
	handled separately according to it's current state. 
	"""
        ACTIONS = { ("CM","replace"):("Replacing","Replaced attribute '%s' in dn: %s"),
                    ("CM","delete"):("Deleting","Deleted: %s"),
		    ("CM","add"):("Adding","Added: %s"),
		    ("DN","newrdn"):("Moving","Moved: %s"),
		    ("DN","deloldrdn"):("Removing","Removed: %s"),
		    ("CD",""):("Deleting","Deleted: %s"),
		    ("CA",""):("Adding","Added: %s")}

	error = message = ""
	if env.LDBUG:
		try:
			ldap.set_option(ldap.OPT_DEBUG_LEVEL, 4095)
			options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
			ldap.set_option(*options[0])
			connection = ldap.initialize(env.LDAPSERVER, trace_level=2)
			connection.simple_bind_s(env.BINDDN, env.LDAPPW)
		except ldap.LDAPError, error:return "Unable to bind to %s with %si. (Wrong credentials?)" % (env.LDAPSERVER, env.BINDDN)
	else:
		try:
			options = [(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)]
			ldap.set_option(*options[0])
			connection = ldap.initialize(env.LDAPSERVER)
			connection.simple_bind_s(env.BINDDN, env.LDAPPW)
		except ldap.LDAPError, error:return "Unable to bind to %s with %s. (Wrong credentials?)" % (env.LDAPSERVER, env.BINDDN)
	# Get (dictionairy-)content and devide in dn containers.
	for transaction in content:
		for dn,entry in transaction.items():
			time.sleep(0.015)
			# Reset STATES
			STATE = STATEKEY = newrdn = deloldrdn = "" 
			# CM CA CD, Changetype modify, add and delete.
			# add, delete, replace, (STATEKEY) are modification types.
			for key in entry.keys():
				if key == "changetype" and entry[key][0] == "moddn":STATE = "DN"
				if key == "changetype" and entry[key][0] == "modify":STATE = "CM"
				if key == "changetype" and entry[key][0] == "add":STATE = "CA"
				if key == "changetype" and entry[key][0] == "delete":STATE = "CD"
				if key == "add":STATEKEY = key 
				if key == "delete":STATEKEY = key
				if key == "replace":STATEKEY = key
				if key == "newrdn":newrdn = entry[key][0]; STATEKEY = key
				if key == "deloldrdn":deloldrdn = entry[key][0]; STATEKEY = key
				if key == "objectclass":STATE = "CA"; # Nearly no ldif uses 'changetype: add' anymore!
			try:
		        	# Changetype Modify, CM
				if   STATE == "DN" and newrdn != "":
					time.sleep(0.3)
					if deloldrdn == 0:
						connection.modrdn_s(dn, newrdn, delold = 0)
					else:
						connection.modrdn_s(dn, newrdn, delold = 1)
					time.sleep(0.3)
				elif STATE == "CM" and STATEKEY == "replace":
					values = [( ldap.MOD_REPLACE, key, entry[key][0] )]	
					connection.modify_s(dn,values)
			        elif STATE == "CM" and STATEKEY == "delete":
					values = [( ldap.MOD_DELETE, key, entry[key] )]
					connection.modify_s(dn,values)
			        elif STATE == "CM" and STATEKEY == "add":
					values = [( ldap.MOD_ADD, key, entry[key] )]
					connection.modify_s(dn,values)
				# Changetype Delete, CD 
				elif STATE == "CD" and STATEKEY == "": 
		                	connection.delete_s(dn)
				# Changetype Add, CA
				elif STATE == "CA" and STATEKEY == "":
					values = modlist.addModlist(entry)
					connection.add_s(dn,values)
				else:
					continue
				if STATEKEY == "replace":
					if env.VERBOSE:print ACTIONS[(STATE,STATEKEY)][1] % key,dn
				elif env.VERBOSE:print ACTIONS[(STATE,STATEKEY)][1] % dn
			except ldap.LDAPError, error:
				REASON = "%s\n" % error.message['desc']
	                        message += "ERROR %s dn: %s REASON: %s" % (ACTIONS[(STATE,STATEKEY)][0],dn,REASON)
				if not env.CONTINUEONERROR:
					connection.unbind()
					return message
	connection.unbind_s()
	if error == "":error="OK"
	else: error = message
	return error

# Open the file 'fname' and return its contents and error state.
def read(fname):
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
	return content,error

# Main program. Take cmd arguments and call functions....
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This program takes an ldif file as input and commits it to an ldap server.')
	parser.add_argument('filename', action='store', nargs=1, metavar='filename', help='LDIF file.')
	parser.add_argument('--host', action='store', metavar='hostname', help='LDAP servername or ip-adress.')
	parser.add_argument('--binddn', action='store', metavar='dn', help='Distinguist name of bind user.')
	parser.add_argument('--quiet', action='store_false', default=True, dest='quiet', help='Only show errors.')
	parser.add_argument('--ldbug', action='store_true', default=False, dest='ldbug', help='Show LDAP debug information.')
	parser.add_argument('--coer', action='store_false', default=True, dest='coer', help='Continue after commit error (e.g. OBJECT NOT AVAILABLE.)')
	parser.add_argument('-W', action='store_true', default=False, dest='passwordprompt', help='Prompt for bind password.')
	args = vars(parser.parse_args())
	fname = args['filename'][0]
	env = environment()
	env.LDAPSERVER = args['host']
	env.BINDDN = args['binddn']
	if args['passwordprompt'] == False:
		error = "ERROR: No bind password provided."
		print error
		exit(1)

	env.CONTINUEONERROR = args['coer']
	env.VERBOSE = args['quiet']
	env.LDBUG = args['ldbug']
	
	if args['passwordprompt']:
		print env.BINDDN
		env.LDAPPW = getpass.getpass()
	content,error = read(fname)
	if error != "OK":print error
	else:
		content,error=ldif2dict(content)
		if error != "OK":print error
		else:
			error=apply_ldif(content,env)
			if error != "OK":print error
