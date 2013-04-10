#!/bin/bash
FILENAME="`date +%s`.ldif"
cat << EOF > $FILENAME
dn: olcDatabase={-1}frontend,cn=config
changeType: modify
replace: olcSizeLimit
olcSizeLimit: 3000

EOF
ldapadd -Y EXTERNAL -H ldapi:/// -f $FILENAME && rm $FILENAME
