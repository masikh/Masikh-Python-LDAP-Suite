#!/bin/bash
FILENAME="/tmp/`date +%s`.ldif"
cat << EOF > $FILENAME
dn: cn=autofs,cn=schema,cn=config
objectClass: olcSchemaConfig
cn: autofs
olcObjectClasses: {0}( 1.3.6.1.1.1.1.13 NAME 'automount' DESC 'An entry in an 
 automounter map' SUP top STRUCTURAL MUST ( cn $ automountInformation $ object
 class ) MAY description )
olcObjectClasses: {1}( 1.3.6.1.4.1.2312.4.2.2 NAME 'automountMap' DESC 'An gro
 up of related automount objects' SUP top STRUCTURAL MUST ou )
EOF
ldapadd -Y EXTERNAL -H ldapi:/// -f $FILENAME && rm $FILENAME
