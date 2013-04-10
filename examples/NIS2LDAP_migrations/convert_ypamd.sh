#!/bin/bash
for uid in `ypcat passwd | awk -F: {'print $1'}`; do
	EXPORT="`ypmatch $uid auto.home`"
	echo "dn: cn=$uid,ou=auto.home,ou=autofs,dc=unix,dc=liacs,dc=nl"
	echo "cn: $uid"
	echo "objectClass: top"
	echo "objectClass: automount"
	echo "automountInformation: -soft,intr,nosuid $EXPORT"
	echo
done
