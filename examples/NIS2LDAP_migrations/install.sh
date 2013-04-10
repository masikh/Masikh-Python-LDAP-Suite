#!/bin/sh
./add-automount-support.sh
./add-autofs-support.sh
./ldap-import.sh master.ldif
./ldap-import.sh ypamd.ldif
./ldap-import.sh ypgrp.ldif
./ldap-import.sh yppwd.ldif
./ldap-import.sh netgroup.ldif
