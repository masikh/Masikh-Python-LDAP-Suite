#!/bin/sh
for group in `ypcat group`; do
	# Declare some attribute variable
	cn="`echo $group | awk -F: {'print $1'}`"	
	userPassword="`echo $group | awk -F: {'print "{crypt}"$2'}`"
	gidNumber="`echo $group | awk -F: {'print $3'}`"
	
	# Print DN header and attributes
	echo "dn: cn=$cn,ou=Group,dc=unix,dc=liacs,dc=nl"
	echo "objectClass: posixGroup"
	echo "objectClass: top"
	echo "cn: $cn"
	echo "userPassword: $userPassword"
	echo "gidNumber: $gidNumber"

#	# Group membership assignment
#	case "$cn" in
#	staff)
#		for member in `ypcat passwd`; do
#			echo $member | grep ":$gidNumber:" | awk -F: {'print "memberUid: "$1'}
#		done
#		;;
#	student)
#		for member in `ypcat passwd`; do
#			echo $member | grep ":$gidNumber:" | awk -F: {'print "memberUid: "$1'}
#		done
#		;;
#	bijvak)
#		for member in `ypcat passwd`; do
#			echo $member | grep ":$gidNumber:" | awk -F: {'print "memberUid: "$1'}
#		done
#		;;
#	iee)
#		for member in `ypcat passwd`; do
#			echo $member | grep ":$gidNumber:" | awk -F: {'print "memberUid: "$1'}
#		done
#		;;
#	iib)
#		for member in `ypcat passwd`; do
#			echo $member | grep ":$gidNumber:" | awk -F: {'print "memberUid: "$1'}
#		done
#		;;
#	media)
#		for member in `ypcat passwd`; do
#			echo $member | grep ":$gidNumber:" | awk -F: {'print "memberUid: "$1'}
#		done
#		;;
#	sbb)
#		for member in `ypcat passwd`; do
#			echo $member | grep ":$gidNumber:" | awk -F: {'print "memberUid: "$1'}
#		done
#		;;
#	
#	*)	
		members="`echo $group | awk -F: {'print $4'} | sed s/,/\ /g`"
		for member in $members; do
			echo "memberUid: $member"
		done
#		;;
#	esac
	echo
done
