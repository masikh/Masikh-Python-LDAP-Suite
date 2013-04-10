#!/bin/bash
FILENAME="`date +%s`.ldif"
cat << EOF > $FILENAME
dn: cn={2}nis,cn=schema,cn=config
changetype: modify
delete: olcObjectClasses
olcObjectClasses: {0}( 1.3.6.1.1.1.2.0 NAME 'posixAccount' DESC 'Abstraction of an account with POSIX attributes' SUP top AUXILIARY MUST ( cn $ uid $ uidNumber $ gidNumber $ homeDirectory ) MAY ( userPassword $ loginShell $ gecos $ description ) )

dn: cn={2}nis,cn=schema,cn=config
changetype: modify
add: olcAttributeTypes
olcAttributeTypes: {25}( 1.3.6.1.1.1.1.25 NAME 'automountInformation' DESC 'Information used by the autofs automounter' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE )

dn: cn={2}nis,cn=schema,cn=config
changetype: modify
add: olcObjectClasses
olcObjectClasses: {0}( 1.3.6.1.1.1.2.0 NAME 'posixAccount' DESC 'Abstraction of an account with POSIX attributes' SUP top AUXILIARY MUST ( cn $ uid $ uidNumber $ gidNumber $ homeDirectory ) MAY ( userPassword $ loginShell $ gecos $ description $ automountInformation ) )

EOF
ldapadd -Y EXTERNAL -H ldapi:/// -f $FILENAME && rm $FILENAME
