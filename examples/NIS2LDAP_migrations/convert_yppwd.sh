#!/bin/sh
IFS="
"
for user in `ypcat passwd`; do
	# Declare some attribute variable
	uid="`echo $user | awk -F: {'print $1'}`"	
	cn="`echo $user | awk -F: {'print $5'}`"	
	sn="`echo $user | awk -F: {'print $5'}`"	
	userPassword="`echo $user | awk -F: {'print $2'}`"	
	loginShell="`echo $user | awk -F: {'print $7'}`"	
	uidNumber="`echo $user | awk -F: {'print $3'}`"	
	gidNumber="`echo $user | awk -F: {'print $4'}`"	
	homeDirectory="`echo $user | awk -F: {'print $6'}`"	
	gecos="`echo $user | awk -F: {'print $5'}`"	
	
	# Print DN header and attributes
	echo "dn: uid=$uid,ou=People,dc=unix,dc=liacs,dc=nl"
	echo "uid: $uid"
	# Get first field (before a possible studentnumber)
	echo -n "cn: "
	echo $cn | awk -F, {'print $1'} | awk {'print $1'}
	# Get second till last field (before a possible studentnumber)
	echo -n "sn: "
	echo $sn | awk -F, {'print $1'} | awk -vORS=' ' {'for (i=2; i<=NF; i++) print $i'} | sed s/\ $// ; echo
	echo "objectClass: inetOrgPerson"
	echo "objectClass: posixAccount"
	echo "objectClass: shadowAccount"
	echo "userPassword: {crypt}$userPassword"
	echo "loginShell: $loginShell"
	echo "uidNumber: $uidNumber" 
	echo "gidNumber: $gidNumber"
	echo "homeDirectory: $homeDirectory"
	# Get all field before possible studentnumber
	echo $gecos | awk -F, {'print "gecos: "$1'}
	# Write studentnumber into employeeNumber attribute else $gidNumber.$uidNumber
	if [ "_`echo $gecos | awk -F, {'print $2'}`" = "_" ]; then
		echo "employeeNumber: $gidNumber.$uidNumber";
	else
		temp="`echo $gecos | awk -F, {'print $2'}`"
		echo $temp | grep [0-9] > /dev/null
		if [ $? -ne 0 ] ; then
		        echo "employeeNumber: $gidNumber.$uidNumber"
		else
			echo $gecos | awk -F, {'print "employeeNumber: "$2'}
		fi
	fi
	# Write accounttype into employeeType attribute
	case "$gidNumber" in
	100)
		echo "employeeType: Staf"
		;;
	200)
		echo "employeeType: Gast"
		;;
	500)
		echo "employeeType: Student"
		;;
	600)
		echo "employeeType: Bijvak"
		;;
	900)
		echo "employeeType: DBA"
		;;
	*)
		echo "employeeType: ComputerAccount-$gidNumber"
		;;
	esac
	echo
done
