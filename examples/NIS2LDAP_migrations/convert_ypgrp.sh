#!/bin/sh
for group in `ypcat group`; do
	# Declare some attribute variable
	cn="`echo $group | awk -F: {'print $1'}`"	
	userPassword="`echo $group | awk -F: {'print "{crypt}"$2'}`"
	gidNumber="`echo $group | awk -F: {'print $3'}`"
	
	# Print DN header and attributes
	echo "dn: cn=$cn,ou=Group,dc=unix,dc=example,dc=nl"
	echo "objectClass: posixGroup"
	echo "objectClass: top"
	echo "cn: $cn"
	echo "userPassword: $userPassword"
	echo "gidNumber: $gidNumber"
	members="`echo $group | awk -F: {'print $4'} | sed s/,/\ /g`"
	for member in $members; do
		echo "memberUid: $member"
	done
	echo
done
