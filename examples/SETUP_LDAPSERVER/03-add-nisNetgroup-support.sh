#!/bin/bash
FILENAME="`date +%s`.ldif"
cat << EOF > $FILENAME
dn: cn={2}nis,cn=schema,cn=config
changetype: modify
delete: olcattributetypes
olcattributeTypes: ( 1.3.6.1.1.1.1.14 NAME 'nisNetgroupTriple' DESC 'Netgroup triple' SYNTAX 1.3.6.1.1.1.0.0 )

dn: cn={2}nis,cn=schema,cn=config
changetype: modify
add: olcattributetypes
olcattributeTypes: ( 1.3.6.1.1.1.1.14 NAME 'nisNetgroupTriple' DESC 'Netgroup triple' EQUALITY caseIgnoreIA5Match SUBSTR caseIgnoreIA5SubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )

EOF
ldapadd -Y EXTERNAL -H ldapi:/// -f $FILENAME && rm $FILENAME
