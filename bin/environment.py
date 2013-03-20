#!/usr/bin/env python

# Copyright:      Copyright 2013 Robert Nagtegaal
#                 Robert Nagtegaal <masikh@gmail.com>
#                 This program is distributed under the terms of the GNU 
#                 General Public License (or the Lesser GPL)

#
# WARNING:	  THIS FILE CONTAINS PASSWORD (NOT NEEDED BTW) THUS KEEP
#		  THE FILE SECURITY TIGHT! (e.g. 600 -rw-------)

class environment:
	def __init__( self,
		      CWD = "",
		      LOGS = "./../LOGS/",
		      ACCOUNTFORM = "./../FORMS/",
		      LDAPPW = "YOURVERYSECRETPASSWORDHERE",
		      LDAPSERVER = "ldap.unix.example.nl",
		      LDBUG = False,
		      VERBOSE = False,
		      BASEDN = "dc=unix,dc=example,dc=nl",
		      BINDDN = "cn=admin,",
		      CONTINUEONERROR = True):

		self.CWD = CWD
		self.LOGS = CWD + LOGS
		self.ACCOUNTFORM = CWD + ACCOUNTFORM
		self.LDAPPW = LDAPPW
		self.LDAPSERVER = LDAPSERVER
		self.LDBUG = LDBUG
		self.VERBOSE = VERBOSE
		self.BASEDN = BASEDN
		self.BINDDN = BINDDN + BASEDN
		self.CONTINUEONERROR = True

	@classmethod 
	def group_ranges(self, typeset):
		self.ranges = { 'primary': ['100','999'],
		                'secondairy': ['11100', '13999'] }
		return self.ranges[typeset][0],self.ranges[typeset][1]

	def user_ranges(self):
		self.ranges = { 'Staff': ['100','10000','12000'],
		                'Guest': ['200','5000','6000'],
		                'AIO/PHD': ['600','9001','9999'],
		                'Student': ['500','6000','9000'] }
		return self.ranges

	def user_netgroups(self):
		self.netgroups = { 'Staff': ['users-sil'],
				   'Guest' : ['users-sil'],
				   'AIO/PHD' : ['users-sil', 'users-pc302', 'users-pc303', 'users-pc306', 'users-cdh'],
				   'Student' : ['users-sil', 'users-pc302', 'users-pc303', 'users-pc306', 'users-cdh'] }
		return self.netgroups

	def user_exports(self):
		self.exports = { 0 : ["Staff leden","-soft,intr,nosuid nfs-server01:/users/staff:&"],
				 1 : ["Student 2013","-soft,intr,nosuid nfs-server02:/users/13/student:&"],
				 2 : ["Student 2014","-soft,intr,nosuid nfs-server02:/users/14/student:&"],
				 3 : ["Student 2015","-soft,intr,nosuid nfs-server02:/users/15/student:&"],
				 4 : ["Student 2016","-soft,intr,nosuid nfs-server02:/users/16/student:&"],
				 5 : ["Student 2017","-soft,intr,nosuid nfs-server02:/users/17/student:&"],
				 6 : ["Student 1999","-soft,intr,nosuid nfs-server02:/users/99/student:&"],
				 7 : ["Student 2000","-soft,intr,nosuid nfs-server02:/users/00/student:&"],
				 8 : ["Student 2001","-soft,intr,nosuid nfs-server02:/users/01/student:&"],
				 9 : ["Student 2002","-soft,intr,nosuid nfs-server02:/users/02/student:&"],
				10 : ["Student 2003","-soft,intr,nosuid nfs-server02:/users/03/student:&"],
				11 : ["Student 2004","-soft,intr,nosuid nfs-server02:/users/04/student:&"],
				12 : ["Student 2005","-soft,intr,nosuid nfs-server02:/users/05/student:&"],
				13 : ["Student 2006","-soft,intr,nosuid nfs-server02:/users/06/student:&"],
				14 : ["Student 2007","-soft,intr,nosuid nfs-server02:/users/07/student:&"],
				15 : ["Student 2008","-soft,intr,nosuid nfs-server02:/users/08/student:&"],
				16 : ["Student 2009","-soft,intr,nosuid nfs-server02:/users/09/student:&"],
				17 : ["Student 2010","-soft,intr,nosuid nfs-server02:/users/10/student:&"],
				18 : ["Student 2011","-soft,intr,nosuid nfs-server02:/users/11/student:&"],
				19 : ["Student 2012","-soft,intr,nosuid nfs-server02:/users/12/student:&"],
				20 : ["Student OLD","-soft,intr,nosuid nfs-server02:/users/old/student:&"]
		}
		return self.exports
