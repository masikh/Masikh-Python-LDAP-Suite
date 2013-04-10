#!/bin/bash
FILENAME="`date +%s`.ldif"
cat << EOF > $FILENAME
dn: olcDatabase={1}hdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: uidNumber eq
olcDbIndex: gidNumber eq
olcDbIndex: loginShell eq
olcDbIndex: uid eq,pres,sub
olcDbIndex: memberUid eq,pres,sub
olcDbIndex: uniqueMember eq,pres
olcDbIndex: nisNetgroupTriple eq,pres,sub

EOF
ldapadd -Y EXTERNAL -H ldapi:/// -f $FILENAME && rm $FILENAME
