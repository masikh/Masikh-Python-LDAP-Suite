## User manual for Masikh's Python LDAP Suite (MPLS)

### Screenshots

![Some menu's](/Overview.png "Overview")

![Add Multiple users](/Add-users.png "Add multiple users")

### contents:

- [Conventions used in this manual](#conventions)  
- [A short introduction into MPLS](#test)  
- [General usage](#generalusage)  
  - [Navigate through the program](#generalusage-navigate) 
  - [Color usage and its function](#generalusage-colorusage)
  - [Bread crumbs](#generalusage-breadcrumbs)
  - [Input validation](#generalusage-inputvalidation)
  - [Leaving a sub-module (part of the program)](#generalusage-leaving)
  - [Terminal size](#generalusage-terminalsize)
- [Overview of MPLS options](#mplsoptions)  
- [Search menu](#searchmenu)  
  - [Search -> User](#searchmenu-user)
    - [-> User -> By part of username](#searchmenu-user-partof)
    - [-> User -> Information](#searchmenu-user-information)
    - [-> User -> Query Autofs](#searchmenu-user-autofs)
  - [Search -> Group](#searchmenu-group)
    - [-> Group -> Show all groups](#searchmenu-group-all)
    - [-> Group -> By user name](#searchmenu-group-byuser)
    - [-> Group -> By group name](#searchmenu-group-byname)
  - [Search -> Netgroup](#searchmenu-netgroup)
    - [-> Netgroup -> Show all netgroups](#searchmenu-netgroup-all)
    - [-> Netgroup -> Show membership](#searchmenu-netgroup-membership)
    - [-> Netgroup -> Information](#searchmenu-netgroup-information)
  - [Search -> Transactions](#searchmenu-transactions)
- [Modify menu](#modifymenu)  
- [Login menu](#loginmenu)  
- [Help menu](#helpmenu)  
- [Exit](#exit)  
- [Configuring MPLS for your environment (uidNumber ranges, etc...)](#environment)  
- [What is a 'user', 'group' or 'netgroup anyway?](#whatis)  
- [About & Copyrights](#gpl)  

## <a name="conventions" />Conventions used in this manual
Every item within brackets is user input. E.g. [fverbeek], in this case
'fverbeek' is user input (without the brackets!!!).

## <a name="introductionmpls" />A short introduction into MPLS
MPLS is a user account tool for LDAP. It stands-out of other LDAP software
because it handles NIS-netgroups and has a transaction undo feature.

MPLS is meant as a unified tool for LDAP manipulations. Unified means that
it's build to accommodate the needs of 'users', 'help-desk' and 'system-
administrators.' MPLS tries to simplify standard daily tasks but also the
somewhat complex tasks. E.g. renaming a user and make sure its (net-)group
memberships are preserved. Every transaction made to the LDAP database
from MPLS is logged and made undo-able. Thus if you delete a user or some-
thing else you can easily undo this. This is part of the philosophy of
MPLS. 

Another philosophy behind MPLS is: Every helper-program should be callable
from MPLS and the CLI. Every helper-program (helpers) has a set of
'command-line arguments' you can set. This is obviously not needed when
you call these helpers from within MPLS. Because every helper is a stand-
alone unit (like UNIX tools) MPLS is easily expendable.

There is a unified menu-structure which is trivially expandable with new 
items. The menu-structure as such has nothing to do with MPLS as whole but
is rather a convenient method of presenting helpers to a user. See chapter
'Further Development' for more in-depth information.

MPLS is by no means a complete product. It aims at taking away the burden 
of repetitive account tasks and delegating tasks to appropriate skilled
personnel.

MPLS has no security whatsoever. The security of this tool is handled by
the mechanisms already in place on the target systems. E.g. You can
access this tool via SSH protocol (Just make it the default shell of a 
'special user'). SSH is charged with the security not MPLS! Every
connection made to the LDAP server is done with the security measures 
imposed by the LDAP server itself (e.g. SSL/TLS) not MPLS. The
philosophy of MPLS is: Make security not the problem of MPLS but that of
the systems MPLS interacts with.

## <a name="generalusage" />General usage
### <a name="generalusage-navigate" />Navigate through the program
	
Moving around in the program can be done in several ways
	
* Hot keys. Hot keys are marked as red letters. Typing such a let-
  ter will automaticly select the appropriate menu item within the
  current sub menu.

* Arrow keys. Arrow keys can be used to navigate through the menu-
  structure. Note the behavior of the arrow keys change between
  horizontal and vertical menus. E.g. In a horizontal menu (top-
  menu) the down-arrow opens an item but in a vertical menu the
  right-arrow opens a menu-item.

### <a name="generalusage-colorusage" />Color usage and its function

Through out the whole program there is a consistent color usage.
	
* Text in the color RED always means an action or a warning. E.g.
	Enter username: ....

* Text in the color WHITE is informational in nature. E.g.
	Bread-crumbs at the bottom of the screen.

* Blocked text in the color WHITE means your current active menu
  item. E.g.
	Query by (part of) username

### <a name="generalusage-breadcrumbs" />Bread crumbs

Through out the whole program you can easily see where you are 
in terms of the menu-structure. Every step in the menu-structure
will leave a bread-crumb. Thus it leaves a trail. These crumbs 
are printed in the left-bottom of the screen. If the trail gets
to long, the begin is truncated as dots 

### <a name="generalusage-inputvalidation" />Input validation

Every editable item in this program (e.g. enter username:) is
validated on proper input. This works mostly but probably not 
always, be warned! If a user enters an invalid input, the user
gets a warning. This warning looks like: 
	
(Wrong input: Use -.+=, a-z A-Z 0-9 only)

This warning is displayed at the bottom of the active screen
       in the color RED

### <a name="generalusage-leaving" />Leaving a sub-module (part of the program)

Most of the time people are 'just browsing around' through the
program. If you enter one of the sub-modules (e.g. Add user)
you can simply bail out by pressing [esc] or give empty input
(e.g. [enter])
	
### <a name="generalusage-terminalsize" />Terminal size

MPLS has been designed to work in a standard 'telnet' window.
These windows are typically 80 characters wide and 24 lines long
(80x24). A larger window is not a problem, but MPLS ~WILL CRASH~
if you make the terminal window smaller than 80x24. This has
nothing to do with MPLS but rather the underlying (n)Curses
interface. 

## <a name="mplsoptions" />Overview of MPLS options

MPLS has five top-level menu items: Search, Modify, Login, Help
and Exit. The two most important are Search and Modify.

*	Search: In this menu you can query for user, group or
	NIS-netgroups items. Furthermore, you can query all
	transactions/modifications on the LDAP database via MPLS.

*	Modify: In this menu you can modify user(s), group(s)
	and NIS-Netgroups. Furthermore, you can query, view and
	undo transactions/modifications on the LDAP database via
	MPLS.
	
*	Login: From here you can bind to a different LDAP server
	Then the default server. (The Default server is	configured
	in the MPLS environment file; environment.py)

*	Help menu: You can browse through these help-pages.

*	Exit: Every program needs a stop condition. This is the
	one!

## <a name="searchmenu" />Search menu

In this menu you can query for user, group or NIS-netgroups items.
Furthermore, you can query all transactions/modifications on the
LDAP database via MPLS.

### <a name="searchmenu-user" />Search -> User

In this sub menu you can query for a user or user specific items.

### <a name="searchmenu-user-partof" />-> User -> By part of username

With this helper you can look-up an username if you only know part
of its name.

Example usage:

1: Enter username: [ert]

result:

dn: uid=labert,ou=People,dc=unix,dc=example,dc=org  
dn: uid=lerts,ou=People,dc=unix,dc=example,dc=org  
dn: uid=robert,ou=People,dc=unix,dc=example,dc=org

### <a name="searchmenu-user-information" />-> User -> Information

With this helper you can lookup all attributes of a single user.

Example usage:

1: Enter username: [robert]

result:

dn: uid=robert,ou=People,dc=unix,dc=example,dc=org  
employeeType: Staff  
uid: robert  
objectClass: inetOrgPerson  
objectClass: posixAccount  
objectClass: shadowAccount  
loginShell: /bin/bash  
uidNumber: 58430  
gidNumber: 100  
gecos: R.D.A. Nagtegaal.  
sn: Nagtegaal  
homeDirectory: /home/robert  
cn: Robert  
employeeNumber: 100.58430  

Note: employeeNumber is either a concatenation of gidNumber and
uidNumber or a student registration number.

### <a name="searchmenu-user-autofs" />-> User -> Query Autofs

With this helper you can lookup all exports for this user known in
the LDAP database. Thus all autofs entries.

Example usage:

1: Enter username: [robert]  

result:  

dn: cn=robert,ou=auto.home,ou=Autofs,dc=unix,dc=example,dc=org  
-soft,intr,nosuid nfs-server01:/users/staff:&  
  
dn: cn=/scratch,ou=auto.direct,ou=Autofs,dc=unix,dc=example,dc=org  
scratch.example.org:/scratch  
  
dn: cn=/var/spool/mail,ou=auto.direct,ou=Autofs,dc=unix,dc=example,dc=org  
mailhost.example.org:/var/spool/mail  
  
dn: cn=/appl,ou=auto.direct,ou=Autofs,dc=unix,dc=example,dc=org  
nfs-server01.example.org,nfs-server02.example.org:/appl  

Note: The user 'Robert' has one home-directory and three other
exports, /scratch, /var/spool/mail and /appl. The respective
exporting servers are: nfs-server01 and nfs-server02.

### <a name="searchmenu-group" />Search -> Group

In this menu you can query group information. You can show all
available groups, the groups a user is member of and the users in a
certain group.

### <a name="searchmenu-group-all" />-> Group -> Show all groups

With this helper you can lookup all groups

Example usage:

Use your arrow keys to scroll through all available groups and use
escape to exit this helper.

result:

...  
dn: cn=acmmm,ou=Group,dc=unix,dc=example,dc=org  
dn: cn=admin,ou=Group,dc=unix,dc=example,dc=org  
dn: cn=afddoc,ou=Group,dc=unix,dc=example,dc=org  
dn: cn=afdrap,ou=Group,dc=unix,dc=example,dc=org  
dn: cn=alumni,ou=Group,dc=unix,dc=example,dc=org  
dn: cn=apparc,ou=Group,dc=unix,dc=example,dc=org  
...  

### <a name="searchmenu-group-byuser" />-> Group -> By user name

With this helper you can lookup groups assign to a user.

Example usage:

Enter username: [fverbeek]

result:

gidNumber Primary group DN for user fverbeek  
========= ==================================  
100       dn: cn=staff,ou=Group,dc=unix,dc=example,dc=org  
  
gidNumber Non-primary groups DNs for user fverbeek  
========= ==================================   
11177     dn: cn=cshrpr,ou=Group,dc=unix,dc=example,dc=org  
11147     dn: cn=cszebra,ou=Group,dc=unix,dc=example,dc=org  
11185     dn: cn=csstuva,ou=Group,dc=unix,dc=example,dc=org  
11175     dn: cn=csbpn,ou=Group,dc=unix,dc=example,dc=org  
11153     dn: cn=cshci,ou=Group,dc=unix,dc=example,dc=org  
11192     dn: cn=csre,ou=Group,dc=unix,dc=example,dc=org  
11144     dn: cn=csbio,ou=Group,dc=unix,dc=example,dc=org  
  
Note: In this example the user 'fverbeek' has primary group  
'staff' with gidNumber '100' and seven secondary groups.  

### <a name="searchmenu-group-byname" />-> Group -> By group name

With this helper you can lookup members of a given group.

Example usage:

Enter groupname: [csdale]

result:

Members of group csdale (gidNumber: 11158)  
======================= =============  
memberUid: csdale  
memberUid: tcocx   

Note: In this example there are two members of the group 'csdale'
being 'csdale' itself and 'tcocx'. Furthermore the gidNumber of
'csdale' is 11158.

### <a name="searchmenu-netgroup" />Search -> Netgroup

In this sub menu you can query for netgroup information. Analogue
to the 'Search -> Group' menu there is an option to view all
netgroups, show user/host membership of a netgroup and child
groups of a netgroup.

### <a name="searchmenu-netgroup-all" />-> Netgroup -> Show all netgroups

This helper gives a list of all available netgroups. 

Example usage:

Use your arrow keys to scroll through all available groups and use
escape to exit this helper.

result:

...  
dn: cn=allse,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=allwi,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=allws,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=cdh000a,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=cdh000b,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=cdh000c,ou=Netgroup,dc=unix,dc=example,dc=nl    
...  

### <a name="searchmenu-netgroup-membership" />-> Netgroup -> Show membership

This helper shows the netgroups a user is member of.

Example usage:

Enter username: [fverbeek]

result:

dn: cn=sun,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=pc156a,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=pc409a,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=users-pc306,ou=Netgroup,dc=unix,dc=example,dc=nl  
dn: cn=users-pc302,ou=Netgroup,dc=unix,dc=example,dc=nl  

Note: In this example the user fverbeek is a member of the netgroups
'sun', 'pc156a', 'pc409a', 'users-pc306 and 'users-pc302'. All
hosts in sun, pc156a etc..are hosts the user fverbeek has access
to.

### <a name="searchmenu-netgroup-information" />-> Netgroup -> Information

This helper shows all information of a given netgroup.

Example usage:

Enter netgroup: [users-pc302]

result:

Distinguished name of netgroup users-pc302  
============================== ===========  
dn: cn=users-pc302,ou=Netgroup,dc=unix,dc=example,dc=nl  

Member nis-groups of nis-group users-pc302  
============================== ===========  

Host triples in netgroup  
============================== ===========  

User triples in netgroup  
============================== ===========  
(-,aakachar,)   (-,aaleman,)    (-,aandreye,)   (-,aandring,)  
(-,aanton,)     (-,aassink,)    (-,abacaoan,)   (-,abaggio,)  
(-,abaihaki,)   (-,abegia,)     (-,abijlsma,)   (-,abom,)  
(-,aboogert,)   (-,abosman,)    (-,acaraghi,)   (-,acavusog,)  
(-,acervell,)   (-,achaibra,)   (-,achinedu,)   (-,aclairmo,)  
(-,acomley,)    (-,adarvish,)   (-,adegroot,)   (-,adejonge,)   

Note: In this example there are only user 'triples' in the
netgroup 'users-pc302'. If we would lookup netgroup 'pc302a' we
can observe that is only has one member nis-group, 'users-pc302'.
Using this mechanism users and hosts are bind-ed together.

### <a name="searchmenu-transactions" />-> Transactions

Every modification from MPLS to a LDAP database is logged in a
transaction. Of every transaction made, there is also an undo file
created. This means that every transaction should be un-doable.

This helper gives an overview of all write-transactions from MPLS
to the LDAP database. Each column in the overview gives specific
information about the transaction

TID: Transaction identification number. It's a UNIX date-stamp in
seconds (thus always incrementing!)

Entity: The user, group or netgroup which is modified.

Date: The transaction date (computed from the TID)

Type: The type of modification made. E.g. add-grp (a unix group is
added), multiple-user-add (a bunch of users was created) etc...

Action: There are three types of actions:

	done: 		This is a transaction done somewhere in
			the past.

	undo: 		For every transaction there exists an undo
			file. The undo transaction is not
			committed (yet) to the LDAP server but can
			be used to undo a past transaction.

	reverted:	These are the undo transactions which has
			been committed. Thus if you commit an undo
			transaction it becomes a reverted
			transaction.

Example usage:

Use your arrow keys to scroll through all available transactions.
Press enter to view the highlighted entry and escape to leave the
helper.

result:

Show transaction

Transaction Entity  Date                  Type              Action  
------------------------------------------------------------------  
1363183419  Bijvak  Wed Mar 13 15:03 2013 multiple-user-add done  
1363183419  Bijvak  Wed Mar 13 15:03 2013 multiple-user-add undo  
1363178314  Student Wed Mar 13 13:38 2013 multiple-user-add done  
1363178314  Student Wed Mar 13 13:38 2013 multiple-user-add undo  
1363176151  masikh  Wed Mar 13 13:02 2013 passwordchange    reverted  
...

## <a name="modifymenu" />Modify menu

The modify menu enables you to modify user, group and netgroup
properties. Furthermore you can view and UNDO past modifications
of the LDAP database done via the MPLS software.

- 5.1	Modify -> User

In this submenu you can add or delete a user. Change a users
password, modify its attributes. Adding users in a batch process
can be done with the 'Add multiple users' helper.

- 5.1.1	-> User -> Add user

With the 'Add user' helper you can add a new user to the LDAP
database. This helper will assign a primary group of choice, a
login shell, uidNumber, employeeNumber, gecos, homedirectory,
common name and automount export.
All these items are free selectable from predefined list (where
applicable) or free text fields.

Example usage:

First enter a new (free) username.

NOTE: If the username is not free, a warning will be issued and
the helper will abort all actions! (e.g. ERROR: User robert
already exists!)

Enter new username: [masikh]

After you press enter the following screen will appear:

employeeType:         Staff
uid:                  masikh
loginShell:           /bin/tcsh
uidNumber:            58441
employeeNumber:       100.58441
gidNumber:            100
gecos:                ---
sn:                   ---
homeDirectory:        /home/masikh
automountInformation: ---
cn:                   --- 

If you change the employeeType, the uidNumber, employeeNumber and
gidNumber will change accordingly. (Use arrow keys to select!)

Example:

* employeeType:         /------------\
  uid:                  | CS-Account |
  loginShell:           | CDH        |
* uidNumber:            |-Bijvak-----|
* employeeNumber:       | Student    |
* gidNumber:            | Gast       |
  gecos:                | Staff      |
  sn:                   \------------/
  homeDirectory:        /home/masikh
  automountInformation: ---
  cn:                   ---

NOTE: An asterix ' * ' will appear before each changed user
attribute.

If you change the automountInformation attribute a list of autofs
exports will be presented. Please choose the appropriate export for
the new user with you arrow keys and press enter to select.

Example:

Select export for account

HINT: Older exports (before 2013) are at the bottom!
-------------------------------------------------------------------
Staff leden      -soft,intr,nosuid nfs-server01:/users/staff:&
Student 2013     -soft,intr,nosuid nfs-server02:/users/13/student:&
Student 2014     -soft,intr,nosuid nfs-server02:/users/14/student:&
Student 2015     -soft,intr,nosuid nfs-server02:/users/15/student:&
Student 2016     -soft,intr,nosuid nfs-server02:/users/16/student:&
...


After you have entered all (needed) attributes for a given user,
you press escape. If you left any attributes blank (---) a
informative warning will be issued E.g.

WARNING: Attribute 'gecos' is not set.
WARNING: Attribute 'sn' is not set.
WARNING: Attribute 'cn' is not set.

If you agree with this warning press 'y' or 'Y' to commit this
transaction. E.g.

Do you wish to add user 'masikh' [y|n]

The user will now be created. You will receive the new password
for the given user and an option to printout an account form.

E.g.

User 'masikh' added successfully!

Login:    masikh
Password: 7D,OB0|4Or

Account form has been saved as: 1363099593.user-add.masikh.ps

Do you wish to print 1363099593.user-add.masikh.ps? [y|n]

You almost always want to print this account form. If you choose
to do so, a list of available CUPS printers will be presented.
Select your printer of choice and printout the account-form. 

NOTE: If you press enter this screen will be erased and there are
NO means to retrieve the password (unless you print the
account form by hand!!!)

NOTE: Per default, no netgroups will be assigned to this new user.
If you wish, you can assign these memberships separately.

- 5.1.2	-> User -> Delete user

This helper enables you to delete a single user. When a user is
deleted an undo-file is created. From this undo-file you can
re-create the user, its (net-)group membership and its autofs
exports.

Example usage:

Enter username: [masikh]

result:

'OK' or 'NO such user!'

NOTE: A transaction is added to the transaction list afterward.

- 5.1.3	-> User -> Change user password

With this helper you can reset a user its password.

Example usage:

Enter username: [masikh]

result:

Password reset: OK
New Password: unZl2gs3VI  

- 5.1.4	-> User -> Modify user attributes

With this helper its possible to change EVERY attribute of a given
user. Yes even the username itself! (mod(r)dn in LDAP terms)

Thus you can change:

EmployeeType, uid, loginShell, sn, uidNumber, gidNumber, gecos,
employeeNumber, homeDirectory, automountInformation and cn.

If you try to rename an username to an existing user, an error will
be reported. E.g.

ERROR Moving dn: uid=masikh,ou=People,dc=unix,dc=example,dc=nl REASON:
Already exists

Example usage:

Enter username: [masikh]

* EmployeeType:         Student
  uid:                  masikh
  loginShell:           /bin/tcsh
  sn:                   ---
* uidNumber:            6948
* gidNumber:            500
  gecos:                Masikh Masih
  employeeNumber:       500.6948
  homeDirectory:        /home/masikh
  automountInformation: -soft,intr,nosuid nfs-server02:/users/13/student:&
  cn:                   ---


Change each attribute you wish and press escape when done. MPLS
will ask you if you'd like to commit these changes. E.g.

Do you wish to commit the changes? [y|n]

'y' will commit the changes made.

NOTE: An astrix ' * ' means a changed attribute.

- 5.1.5	-> User -> Add multiple users

With this helper you can add users in a batch process. You can
cut&paste a list of users from a text file into MPLS and create
these users in one blow.
The source file follows a strict format:

studentnumber:firstname:initials:preposition:surname

E.g. 1292285:Andrada:A.I.::Bacaoanu

The last line is a single "." at the beginning of the line stating
the end of the list of new users.

If an username is already taken, an incrementing number will be
added to this username.

E.g. if abacaoan is taken abacaoan1 will be the next username to
try.

After you pasted the users, two more questions will be asked.
	* EmployeeType (this will divine the primary group)
	* automountInformation (where is the NFS homedir of the
	  new user(s)

Example usage:

Add users

File format: studentnumber:firstname:initials:preposition:surname          

e.g.: 1046853:Ran:R.::An
      1286781:Emmanuel:E.:A:Appiah
      1292285:Andrada:A.I.::Bacaoanu
      . <- End of file marker!!!

 Paste file contents here: 3 lines pasted, 0 lines discarded.
/----------------------------------------------------------------\
|                                                                |
|1046853:Ran:R.::An                                              |
|1046853:Ran:R.::An                                              |
|1286781:Emmanuel:E.:A:Appiah                                    |
|.                                                               |
\----------------------------------------------------------------/

After this two questions about employeeType and
automountInformation will be asked:

* employeeType:         CDH
* automountInformation: -soft,intr,nosuid nfs-server02:/users/13/student:&

Press escape when all is filled in correctly. A do you which to
commit question will be asked. E.g.

Ready to add 3 users, do you wish to continue? [y|n]

Finally you'll be asked if you wish to print the new account-forms
on a CUPS printer of your choice (Highly recommended to answer
yes!!!)

Example:

Queue               Location
-----------------------------------------------------------------
ISSC-P2202-17       Snellius, kamer 47, PAND 2202
ISSC-P2202-19       Snellius, kamer 47, PAND 2202
ISSC-P2202-20       Snellius, kamer 40, PAND 2202
ISSC-P2202-24       Snellius, kamer 404, PAND 2202
ISSC-P2202-33       Snellius, kamer 56, PAND 2202
hp-106-bw           Snellius, kamer 106, PAND 2202

- 5.2	Modify -> Group

In this submenu you can add or delete a group, modify group
properties. You can also add or delete a user to/from a group.

- 5.2.1	-> Group -> Add new group

With this helper you can add a new group to the LDAP database. A
group is either a primairy or secundairy group.
	
NOTE: If you add a primairy group make sure you reflect these
changes in the MPLS environment file also. See chapter
'Configuring MPLS for your environment'

If you try to add an existing group, an error is reported.

Example usage:

Add new group
	
Enter group:   [csdale]
Is this group a primairy group?: [y/n]

result:

'OK' or 'Group csdale already exist!'

- 5.2.2	-> Group -> Delete group

With this helper you can remove a group from the LDAP database. If
you deleted the wrong group the undo feature (transaction logs)
will enable you to fully revert that transaction. With fully is
ment, re-add the group PLUS its group-members.

Example usage:

Enter group:   [csdale]

result:

'OK' or 'No such group'

- 5.2.3	-> Group -> Modify group

With this helper you can modify group attributes. These attributes
are: cn (the group name), gidNumber and the group password.

Example usage:

Enter group:   [csdale]

In a new screen you can change the group attributes: e.g.

cn                csdale
gidNumber         11158
userPassword      {crypt} *

If you're content with the modifications, press escape and commit
the changes by answering 'y' on the question 'Do you wish to
commit changes? [y|[n]]'.

NOTE: This transaction is logged and revertable

- 5.2.4	-> Group -> Link user to group

With this helper you can add a user to a group.

Example usage:

Enter username:   [masikh]
Enter group:      [csdale]

result:

'OK' or 'User masikh already in group csdale'

- 5.2.5	-> Group -> Unlink user from group

With this helper you can remove a user from a group

Example usage:

Enter username:   [masikh]
Enter group:      [csdale]

result:

'OK' or 'User masikh is not a member of group csdale!'

- 5.3	Modify -> Netgroup

In this submenu you can add or delete a netgroup. Furthermore you
can add or remove an entity from a netgroup. An entity is either a
user, host or netgroup itself.

- 5.3.1	-> Netgroup -> Add new netgroup

With this helper you can add a new netgroup to the LDAP database.

Example usage:

Enter netgroup:  [lgm]

result:

'netgroup lgm created' or 'ERROR: netgroup lgm already exists!'

- 5.3.2	-> Netgroup -> Delete netgroup

With this helper you can remove a netgroup from the LDAP
database. 

Example usage:

Enter netgroup:  [lgm]

result:

'OK' or 'ERROR: netgroup lgm does not exists!'

- 5.3.3	-> Netgroup -> Link entity to netgroup -> User to netgroup

With this helper you can add a user to a netgroup.

Example usage:

Enter username:  [masikh]
Enter netgroup:  [users-sil]

result:

'OK' or 'ERROR: netgroup users-sil does not exists!' or 'ERROR:
user masikh does not exists!'

- 5.3.4	-> Netgroup -> Link entity to netgroup -> Host to netgroup

With this helper you can add a hostname to a netgroup.

Example usage:

Enter hostname:  [stoeidoos]
Enter netgroup:  [allwi]

result:

'OK' or 'ERROR: netgroup allwi does not exists!'

- 5.3.5	-> Netgroup -> Link entity to netgroup -> Netgroup to netgroup

With this helper you can add a netgroup to a netgroup (Yes,
recursion!) It gives you the possibility to nest netgroups. This
reduces the amount of netgroups needed to run you business.

Example usage:

Enter parent netgroup:  [allwi]
Enter child netgroup:   [wsstaf]

result:

'OK' or 'ERROR: netgroup .... does not exist!'

- 5.3.6	-> Netgroup -> Unlink entity to netgroup -> User to netgroup
- 5.3.7	-> Netgroup -> Unlink entity to netgroup -> Host to netgroup
- 5.3.8	-> Netgroup -> Unlink entity to netgroup -> Netgroup to netgroup

## <a name="loginmenu" />Login Menu
## <a name="helpmenu" />Help Menu
## <a name="exit" />Exit Menu
## <a name="environment" />Configuring MPLS for your environment (uidNumber ranges, etc...)
## <a name="whatis" />What is a 'user', 'group' or 'netgroup' anyway?

UNIX user:

UNIX is a multiuser system. This means that separate users can
work simultaneously on the same hardware. In order to distinct
between these users, the concept of a username is devised.
A username is a way to identify which files or processes belongs
to who.

UNIX group:

When many users exist on a system it becomes hard to see which
role each user has. There might be staff members, guests etc..
The group concept is a convenient way to differentiate between
types of users. For instance you can make the groups 'staff',
'students' and 'guest' and place users in their respective group.
In this way it's much more easy to distinguish between users.

UNIX netgroup:

A netgroup defines a network-wide group of hosts and users. Use a
netgroup to restrict access to shared NFS file systems and to
restrict remote login and shell access.

Network groups are stored in a network information services, such
as LDAP, NIS, or NIS+, NOT in a local file.

## <a name="gpl" />About the Author/Programmer and Copyrights

Author:         Robert Nagtegaal  
E-mail:         robert@example.org, masikh@gmail.com  
Copyright:      Copyright 2013 Robert Nagtegaal  
		Robert Nagtegaal <masikh@gmail.com>  
                This program is distributed under the terms of the GNU   
                General Public License (or the Lesser GPL)  

Thanks to:      Maartje Mulder (For putting up with all my absence)
                Kristian Rietveld
                Mattias Holm
                Maarten Derickx
