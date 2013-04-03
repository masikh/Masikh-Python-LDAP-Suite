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
  - [Modifymenu -> User](#modifymenu-user)
    - [-> User -> Add user](#modifymenu-user-adduser)
    - [-> User -> Delete user](#modifymenu-user-deluser)
    - [-> User -> Change user password](#modifymenu-user-password)
    - [-> User -> Modify user attributes](#modifymenu-user-attr)
    - [-> User -> Add multiple users](#modifymenu-user-add-multiple)
  - [Modifymenu -> Group](#modifymenu-group)
    - [-> Group -> Add new group](#modifymenu-group-addgroup)
    - [-> Group -> Delete group](#modifymenu-group-delgroup)
    - [-> Group -> Modify group](#modifymenu-group-modgroup)
    - [-> Group -> Link user to group](#modifymenu-group-adduser)
    - [-> Group -> Unlink user from group](#modifymenu-group-deluser)
  - [Modifymenu -> Netgroup](#modifymenu-netgroup)
    - [-> Netgroup -> Add new netgroup](#modifymenu-netgroup-addgroup)
    - [-> Netgroup -> Delete netgroup](#modifymenu-netgroup-delgroup)
    - [-> Netgroup -> Link entity to netgroup -> User to netgroup](#modifymenu-netgroup-linkuser)
    - [-> Netgroup -> Link entity to netgroup -> Host to netgroup](#modifymenu-netgroup-linkhost)
    - [-> Netgroup -> Link entity to netgroup -> Netgroup to netgroup](#modifymenu-netgroup-linkgroup)
    - [-> Netgroup -> Unlink entity to netgroup -> User to netgroup](#modifymenu-netgroup-unlinkuser)
    - [-> Netgroup -> Unlink entity to netgroup -> Host to netgroup](#modifymenu-netgroup-unlinkhost)
    - [-> Netgroup -> Unlink entity to netgroup -> Netgroup to netgroup](#modifymenu-netgroup-unlinkgroup)
- [Login menu](#loginmenu)  
- [Help menu](#helpmenu)  
- [Exit](#exit)  
- [Configuring MPLS for your environment (uidNumber ranges, etc...)](#environment)  
- [What is a 'user', 'group' or 'netgroup anyway?](#whatis)  
- [About & Copyrights](#gpl)  

## <a name="conventions" />Conventions used in this manual
Every item within brackets is user input.  
E.g. [fbeek], in this case 'fbeek' is user input (without the brackets!!!).

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
	__Enter username: ....__

* Text in the color WHITE is informational in nature. E.g.  
	__Bread-crumbs at the bottom of the screen.__

* Blocked text in the color WHITE means your current active menu item. E.g.  
	__Query by (part of) username__

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
	
__(Wrong input: Use -.+=, a-z A-Z 0-9 only)__

This warning is displayed at the bottom of the active screen in the color RED

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
	
*	Login: From here you can bind to a LDAP server other then
	the default server. (The Default server is configured in
	the MPLS environment file; environment.py)

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

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Query by (part of) username                                                ││
││                                                                            ││
││ Enter username: re                                                         ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Search > User > By part of username]───────────────────────────────────────┘
```

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││dn: uid=aandreye,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=areuneke,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=bbourdre,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=bcarels,ou=People,dc=unix,dc=example,dc=nl                          ││
││dn: uid=bharensl,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=birrer,ou=People,dc=unix,dc=example,dc=nl                           ││
││dn: uid=ccremers,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=csre,ou=People,dc=unix,dc=example,dc=nl                             ││
││dn: uid=csuares,ou=People,dc=unix,dc=example,dc=nl                          ││
││dn: uid=cveffere,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=cvissere,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=eparren,ou=People,dc=unix,dc=example,dc=nl                          ││
││dn: uid=ereehuis,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=eschreud,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=evreeswi,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=fbigarel,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=ftreurni,ou=People,dc=unix,dc=example,dc=nl                         ││
││dn: uid=fvgemere,ou=People,dc=unix,dc=example,dc=nl                         ││
│└─[use arrow keys for scrolling or [ESC] for quit]───────────────────────────┘│
└──[Search > User > By part of username]───────────────────────────────────────┘
```

### <a name="searchmenu-user-information" />-> User -> Information

With this helper you can lookup all attributes of a single user.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Query user Information                                                     ││
││                                                                            ││
││ Enter username: robert                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Search > User > Information]───────────────────────────────────────────────┘
```

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││dn: uid=robert,ou=People,dc=unix,dc=example,dc=nl                           ││
││employeeType: Staff                                                         ││
││cn: Robert                                                                  ││
││objectClass: inetOrgPerson                                                  ││
││objectClass: posixAccount                                                   ││
││objectClass: shadowAccount                                                  ││
││loginShell: /bin/bash                                                       ││
││uidNumber: 11010                                                            ││
││gidNumber: 100                                                              ││
││gecos: Robert Nagtegaal                                                     ││
││sn: Nagtegaal                                                               ││
││homeDirectory: /home/robert                                                 ││
││uid: robert                                                                 ││
││employeeNumber: 100.11010                                                   ││
││                                                                            ││
│└─[use arrow keys for scrolling or [ESC] for quit]───────────────────────────┘│
└──[Search > User > Information]───────────────────────────────────────────────┘

```

__Note:__ employeeNumber is either a concatenation of gidNumber and
uidNumber or a student registration number.

### <a name="searchmenu-user-autofs" />-> User -> Query Autofs

With this helper you can lookup all exports for this user known in
the LDAP database. Thus all autofs entries.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Query Autofs                                                               ││
││                                                                            ││
││ Enter username: robert                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Search > User > Autofs entries]────────────────────────────────────────────┘

```

__Result:__  

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Query Autofs                                                               ││
││                                                                            ││
││ Enter username: robert                                                     ││
││                                                                            ││
││ dn: cn=robert,ou=auto.home,ou=Autofs,dc=unix,dc=example,dc=nl              ││
││ -soft,intr,nosuid nfs-01:/users/beheer:&                                   ││
││                                                                            ││
││ dn: cn=/scratch,ou=auto.direct,ou=Autofs,dc=unix,dc=example,dc=nl          ││
││ scratch.example.nl:/scratch                                                ││
││                                                                            ││
││ dn: cn=/var/spool/mail,ou=auto.direct,ou=Autofs,dc=unix,dc=example,dc=nl   ││
││ mail.example.nl:/var/spool/mail                                            ││
││                                                                            ││
││ dn: cn=/appl,ou=auto.direct,ou=Autofs,dc=unix,dc=example,dc=nl             ││
││ nfs-01.example.nl,nfs-02.example.nl:/appl                                  ││
││                                                                            ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Search > User > Autofs entries]────────────────────────────────────────────┘
```

__Note:__ The user 'Robert' has one home-directory and three other
exports, /scratch, /var/spool/mail and /appl. The respective
exporting servers are: nfs-server01 and nfs-server02.

### <a name="searchmenu-group" />Search -> Group

In this menu you can query group information. You can show all
available groups, the groups a user is member of and the users in a
certain group.

### <a name="searchmenu-group-all" />-> Group -> Show all groups

With this helper you can lookup all groups

__Example usage:__

Use your arrow keys to scroll through all available groups and use
escape to exit this helper.

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││dn: cn=acmmm,ou=Group,dc=unix,dc=example,dc=nl                              ││
││dn: cn=admin,ou=Group,dc=unix,dc=example,dc=nl                              ││
││dn: cn=addoc,ou=Group,dc=unix,dc=example,dc=nl                              ││
││dn: cn=adrap,ou=Group,dc=unix,dc=example,dc=nl                              ││
││dn: cn=alui,ou=Group,dc=unix,dc=example,dc=nl                               ││
││dn: cn=sparc,ou=Group,dc=unix,dc=example,dc=nl                              ││
││dn: cn=csbt,ou=Group,dc=unix,dc=example,dc=nl                               ││
││                                                                            ││
│└─[use arrow keys for scrolling or [ESC] for quit]───────────────────────────┘│
└──[Search > Group > Show all groups]──────────────────────────────────────────┘
```

### <a name="searchmenu-group-byuser" />-> Group -> By user name

With this helper you can lookup groups assign to a user.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Query groups by user                                                       ││
││                                                                            ││
││ Enter username: robert                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Search > Group > By user name]─────────────────────────────────────────────┘
```

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││gidNumber Primairy group DN for user robert                                 ││
││--------- -------------------------------------                             ││
││100       dn: cn=staff,ou=Group,dc=unix,dc=example,dc=nl                    ││
││                                                                            ││
││gidNumber Non-primary groups DNs for user robert                            ││
││--------- -------------------------------------                             ││
││105       dn: cn=ctd,ou=Group,dc=unix,dc=example,dc=nl                      ││
││11100     dn: cn=admin,ou=Group,dc=unix,dc=example,dc=nl                    ││
││11186     dn: cn=stud,ou=Group,dc=unix,dc=example,dc=nl                     ││
││                                                                            ││
│└─[use arrow keys for scrolling or [ESC] for quit]───────────────────────────┘│
└──[Search > Group > By user name]─────────────────────────────────────────────┘
```

Note: In this example the user 'robert' has primary group  
'staff' with gidNumber '100' and three secondary groups.  

### <a name="searchmenu-group-byname" />-> Group -> By group name

With this helper you can lookup members of a given group.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Query group by name                                                        ││
││                                                                            ││
││ Enter groupname: csdale                                                    ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Search > Group > By group name]────────────────────────────────────────────┘
```

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││Members of group csdale (gidNumber: 11158)                                  ││
││-------------------------------------                                       ││
││memberUid: csdale                                                           ││
││memberUid: tcocx                                                            ││
││                                                                            ││
│└─[use arrow keys for scrolling or [ESC] for quit]───────────────────────────┘│
└──[Search > Group > By group name]────────────────────────────────────────────┘
```

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

__Example usage:__

Use your arrow keys to scroll through all available groups and use
escape to exit this helper.

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││dn: cn=cd000a,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000b,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000c,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000d,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000e,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000f,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000g,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000h,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000i,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000j,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000k,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000l,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000m,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
││dn: cn=cd000n,ou=Netgroup,dc=unix,dc=example,dc=nl                          ││
│└─[use arrow keys for scrolling or [ESC] for quit]───────────────────────────┘│
└──[Search > Netgroup > Show all netgroups]────────────────────────────────────┘
```

### <a name="searchmenu-netgroup-membership" />-> Netgroup -> Show membership

This helper shows the netgroups a user is member of.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Query netgroup membership                                                  ││
││                                                                            ││
││ Enter username: robert                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Search > Netgroup > Show Membership]───────────────────────────────────────┘
```

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││dn: cn=sh,ou=Netgroup,dc=unix,dc=example,dc=nl                              ││
││dn: cn=sun,ou=Netgroup,dc=unix,dc=example,dc=nl                             ││
││dn: cn=stoeidoos,ou=Netgroup,dc=unix,dc=example,dc=nl                       ││
││dn: cn=pc56a,ou=Netgroup,dc=unix,dc=example,dc=nl                           ││
││                                                                            ││
│└─[use arrow keys for scrolling or [ESC] for quit]───────────────────────────┘│
└──[Search > Netgroup > Show Membership]───────────────────────────────────────┘
```

Note: In this example the user fbeek is a member of the netgroups
'sun', 'pc156a', 'pc409a', 'users-pc306 and 'users-pc302'. All
hosts in sun, pc156a etc..are hosts the user fbeek has access
to.

### <a name="searchmenu-netgroup-information" />-> Netgroup -> Information

This helper shows all information of a given netgroup.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Query netgroup information                                                 ││
││                                                                            ││
││ Enter netgroup: users-pc302                                                ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Search > Netgroup > Information]───────────────────────────────────────────┘
```

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││Distinguished name of netgroup users-pc302                                  ││
││-------------------------------------                                       ││
││dn: cn=users-pc302,ou=Netgroup,dc=unix,dc=example,dc=nl                     ││
││                                                                            ││
││Member nis-groups of nis-group users-pc302                                  ││
││-------------------------------------                                       ││
││                                                                            ││
││Host triples in netgroup                                                    ││
││-------------------------------------                                       ││
││                                                                            ││
││User triples in netgroup                                                    ││
││-------------------------------------                                       ││
││(-,akacar,)   (-,aleman,)    (-,adrye,)    (-,anding,)                      ││
││(-,aton,)     (-,assink,)    (-,abcaan,)   (-,baggio,)                      ││
││(-,ahaki,)    (-,agia,)      (-,abijla,)   (-,bom,)                         ││
││(-,aogert,)   (-,aman,)      (-,araghi,)   (-,acvuog,)                      ││
││(-,aervel,)   (-,achaib,)    (-,achine,)   (-,aclair,)                      ││
││(-,acomy,)    (-,adarv,)     (-,aroot,)    (-,ajonge,)                      ││
│└─[use arrow keys for scrolling or [ESC] for quit]───────────────────────────┘│
└──[Search > Netgroup > Information]───────────────────────────────────────────┘
```

__Note:__ In this example there are only user 'triples' in the
netgroup 'users-pc302'. If we would lookup netgroup 'pc302a' we
can observe that is only has one member nis-group, 'users-pc302'.
Using this mechanism users and hosts are bind-ed together.

### <a name="searchmenu-transactions" />Search -> Transactions

Every modification from MPLS to a LDAP database is logged in a
transaction. Of every transaction made, there is also an undo file
created. This means that every transaction should be un-doable.

This helper gives an overview of all write-transactions from MPLS
to the LDAP database. Each column in the overview gives specific
information about the transaction

__TID:__ Transaction identification number. It's a UNIX date-stamp in
seconds (thus always incrementing!)  
__Entity:__ The user, group or netgroup which is modified.  
__Date:__ The transaction date (computed from the TID)  
__Type:__ The type of modification made. E.g. add-grp (a unix group is added),
multiple-user-add (a bunch of users was created) etc...  
__Action:__ There are three types of actions:  
__done:__ 	This is a transaction done somewhere in	the past.  
__undo:__ 	For every transaction there exists an undo
		file. The undo transaction is not
		committed (yet) to the LDAP server but can
		be used to undo a past transaction.  
__reverted:__	These are the undo transactions which has
		been committed. Thus if you commit an undo
		transaction it becomes a reverted
		transaction.  

__Example usage:__

Use your arrow keys to scroll through all available transactions.
Press enter to view the highlighted entry and escape to leave the
helper.

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│──┌───────────────┐───────────────────────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Show transaction                                                           ││
││                                                                            ││
││ Transaction  Entity   Date                      Type               Action  ││
││ ────────────────────────────────────────────────────────────────────────── ││
││ 1364222906   robert   Mon Mar 25 15:48:26 2013  modify_user        reverte ││
││ 1364222906   robert   Mon Mar 25 15:48:26 2013  modify_user        done    ││
││ 1364220092   qwertyngpMon Mar 25 15:01:32 2013  del_netgroup_from_ done    ││
││ 1364220092   qwertyngpMon Mar 25 15:01:32 2013  del_netgroup_from_ undo    ││
││ 1364220084   users-silMon Mar 25 15:01:24 2013  del_netgroup_from_ done    ││
││ 1364220084   users-silMon Mar 25 15:01:24 2013  del_netgroup_from_ undo    ││
││ 1364220061   stoeidoosMon Mar 25 15:01:01 2013  del_host_from_netg undo    ││
││ 1364220061   stoeidoosMon Mar 25 15:01:01 2013  del_host_from_netg done    ││
││ 1364220026   robert-qwMon Mar 25 15:00:26 2013  add_user_to_netgro done    ││
││ 1364220026   robert-qwMon Mar 25 15:00:26 2013  add_user_to_netgro undo    ││
││ 1364219969   users-silMon Mar 25 14:59:29 2013  add_netgroup_to_ne undo    ││
││ 1364219969   users-silMon Mar 25 14:59:29 2013  add_netgroup_to_ne done    ││
││                                                                            ││
│└─[Usage: [ESC] abort [ENTER] Show transaction]──────────────────────────────┘│
└──[Search > Transactions ]────────────────────────────────────────────────────┘
```
## <a name="modifymenu" />Modify menu

The modify menu enables you to modify user, group and netgroup
properties. Furthermore you can view and UNDO past modifications
of the LDAP database done via the MPLS software.

### <a name="modifymenu-user" />Modify -> User

In this submenu you can add or delete a user. Change a users
password, modify its attributes. Adding users in a batch process
can be done with the 'Add multiple users' helper.

### <a name="modifymenu-user-adduser" />-> User -> Add user

With the 'Add user' helper you can add a new user to the LDAP
database. This helper will assign a primary group of choice, a
login shell, uidNumber, employeeNumber, gecos, homedirectory,
common name and automount export.
All these items are free selectable from predefined list (where
applicable) or free text fields.

__Example usage:__

First enter a new (free) username.

__NOTE:__ If the username is not free, a warning will be issued and
the helper will abort all actions! (e.g. ERROR: User robert
already exists!)

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add user                                                                   ││
││                                                                            ││
││ Enter new username: masikh                                                 ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > User > Add user]──────────────────────────────────────────────────┘
```

After you press enter the following screen will appear:

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add user                                                                   ││
││                                                                            ││
││*employeeType:         Student                                              ││
││ uid:                  masikh                                               ││
││ loginShell:           /bin/tcsh                                            ││
││*uidNumber:            6929                                                 ││
││*employeeNumber:       500.6929                                             ││
││*gidNumber:            500                                                  ││
││*gecos:                Masikh Masih                                         ││
││*sn:                   Masih                                                ││
││ homeDirectory:        /home/masikh                                         ││
││*automountInformation: -soft,intr,nosuid nfs-01:/users/14/student:&         ││
││*cn:                   Masikh                                               ││
││                                                                            ││
│└─[Press [ESC] when done, [arrow keys] to select and [enter] to edit.]───────┘│
└──[Modify > User > Add user]──────────────────────────────────────────────────┘
```
If you change the employeeType, the uidNumber, employeeNumber and
gidNumber will change accordingly. (Use arrow keys to select!)

__Example:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add user                                                                   ││
││                                                                            ││
││*employeeType:         ┌────────────┐                                       ││
││ uid:                  │ CS-Account │                                       ││
││ loginShell:           │ CDH        │                                       ││
││*uidNumber:            │ Bijvak     │                                       ││
││*employeeNumber:       │ Student    │                                       ││
││*gidNumber:            │ Gast       │                                       ││
││*gecos:                │ Staff      │                                       ││
││*sn:                   └────────────┘                                       ││
││ homeDirectory:        /home/masikh                                         ││
││*automountInformation: -soft,intr,nosuid nfs-01:/users/14/student:&         ││
││*cn:                   Masikh                                               ││
││                                                                            ││
│└─[Use [arrows] to navigate and [enter] to select.]──────────────────────────┘│
└──[Modify > User > Add user]──────────────────────────────────────────────────┘
```
__NOTE:__ An asterix ' * ' will appear before each changed user
attribute.

If you change the automountInformation attribute a list of autofs
exports will be presented. Please choose the appropriate export for
the new user with you arrow keys and press enter to select.

__Example:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Select export for account                                                  ││
││                                                                            ││
││ HINT: Older exports (before 2013) are at the bottom!                       ││
││────────────────────────────────────────────────────────────────────────────││
││ Staff leden      -soft,intr,nosuid nfs-01:/users/staff:&                   ││
││ Student 2013     -soft,intr,nosuid nfs-02:/users/13/student:&              ││
││ Student 2014     -soft,intr,nosuid nfs-02:/users/14/student:&              ││
││ Student 2015     -soft,intr,nosuid nfs-02:/users/15/student:&              ││
││ Student 2016     -soft,intr,nosuid nfs-02:/users/16/student:&              ││
││ Student 2017     -soft,intr,nosuid nfs-02:/users/17/student:&              ││
││ Bijvak 2013      -soft,intr,nosuid nfs-02:/users/13/bijvak:&               ││
││ Bijvak 2014      -soft,intr,nosuid nfs-02:/users/14/bijvak:&               ││
││ Bijvak 2015      -soft,intr,nosuid nfs-02:/users/15/bijvak:&               ││
││ Bijvak 2016      -soft,intr,nosuid nfs-02:/users/16/bijvak:&               ││
││ Bijvak 2017      -soft,intr,nosuid nfs-02:/users/17/bijvak:&               ││
││ IIB 2013         -soft,intr,nosuid nfs-02:/users/13/iib:&                  ││
││                                                                            ││
│└─[Usage: [ESC] quits, [arrows] choose selection, [enter] make selection]────┘│
└──[Modify > User > Add user]──────────────────────────────────────────────────┘
```

After you have entered all (needed) attributes for a given user,
you press escape. If you left any attributes blank (---) a
informative warning will be issued E.g.

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add user                                                                   ││
││                                                                            ││
││ WARNING: Attribute 'gecos' is not set.                                     ││
││ WARNING: Attribute 'sn' is not set.                                        ││
││ WARNING: Attribute 'automountInformation' is not set.                      ││
││ WARNING: Attribute 'cn' is not set.                                        ││
││                                                                            ││
││ Do you wish to add user 'masikh' [y|n]                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > User > Add user]──────────────────────────────────────────────────┘
```

If you agree with this warning press 'y' or 'Y' to commit this transaction. 

The user will now be created. You will receive the new password
for the given user and an option to printout an account form.

E.g.

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add user                                                                   ││
││                                                                            ││
││ User 'masikh' added succesfully!                                           ││
││                                                                            ││
││ Login:    masikh                                                           ││
││ Password: 2~CRVSY|81                                                       ││
││                                                                            ││
││ Account form has been saved as: 1365004233.user-add.masikh.ps              ││
││                                                                            ││
││ Do you wish to print 1365004233.user-add.masikh.ps? [y|n]                  ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > User > Add user]──────────────────────────────────────────────────┘
```

You almost always want to print this account form. If you choose
to do so, a list of available CUPS printers will be presented.
Select your printer of choice and printout the account-form. 

E.g.

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Print account form                                                         ││
││                                                                            ││
││ Queue               Location                                               ││
││────────────────────────────────────────────────────────────────────────────││
││ hp-119-bw           Snellius, kamer 119, PAND 2202                         ││
││ hp-123-c            Snellius, kamer 123, PAND 2202                         ││
││ hp-144-c            Snellius, kamer 144, PAND 2202                         ││
││ hp-145-c            Snellius, kamer 145, PAND 2202                         ││
││ hp-153-bw           Snellius, kamer 153, PAND 2202                         ││
││ hp-155-bw           Snellius, kamer 155, PAND 2202                         ││
││ hp-156-bw           Snellius, kamer 156, PAND 2202                         ││
││ hp-304-bw           Snellius, kamer 302, PAND 2202                         ││
││ hp-410-bw           Snellius, kamer 410, PAND 2202                         ││
││ hp-57-bw            Snellius, kamer 57, PAND 2202                          ││
││ hp204               Snellius, Kamer 204, PAND 2202                         ││
││ hp206a              Snellius, Kamer 206a, PAND 2202                        ││
││                                                                            ││
│└─[Usage: [ESC] quits, [arrows] select printer, [enter] use selected printer]┘│
└──[Modify > User > Add user]──────────────────────────────────────────────────┘
```

__NOTE:__ If you press enter this screen will be erased and there are
NO means to retrieve the password (unless you print the
account form by hand!!!)

__NOTE:__ Per default, no netgroups will be assigned to this new user.
If you wish, you can assign these memberships separately.

### <a name="modifymenu-user-deluser" />-> User -> Delete user

This helper enables you to delete a single user. When a user is
deleted an undo-file is created. From this undo-file you can
re-create the user, its (net-)group membership and its autofs
exports.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Delete user                                                                ││
││                                                                            ││
││ Enter username: masikh                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > User > Delete user]───────────────────────────────────────────────┘
```

__Result:__

'OK' or 'NO such user!'

NOTE: A transaction is added to the transaction list afterward.

### <a name="modifymenu-user-password" />-> User -> Change user password

With this helper you can reset a user its password.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Change password                                                            ││
││                                                                            ││
││ Enter username: masikh                                                     ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Modify > User > Change user password]──────────────────────────────────────┘

```

__Result:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Change password                                                            ││
││                                                                            ││
││ Enter username: masikh                                                     ││
││                                                                            ││
││ Password reset: OK                                                         ││
││ New Password: nPJEEa\qC-                                                   ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Modify > User > Change user password]──────────────────────────────────────┘

```

### <a name="modifymenu-user-attr" />-> User -> Modify user attributes

With this helper its possible to change EVERY attribute of a given
user. Yes even the username itself! (mod(r)dn in LDAP terms)

__Thus you can change:__

EmployeeType, uid, loginShell, sn, uidNumber, gidNumber, gecos,
employeeNumber, homeDirectory, automountInformation and cn.

If you try to rename an username to an existing user, an error will
be reported. E.g.

```bash
ERROR Moving dn: uid=masikh,ou=People,dc=unix,dc=example,dc=nl REASON:
Already exists
```

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Modify user attributes                                                     ││
││                                                                            ││
││ Enter username: masikh                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > User > Modify user attributes]────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Modify user attributes                                                     ││
││                                                                            ││
││*employeeType:         Student                                              ││
││ uid:                  masikh                                               ││
││*loginShell:           /bin/bash                                            ││
││*uidNumber:            6929                                                 ││
││*employeeNumber:       500.6929                                             ││
││*gidNumber:            500                                                  ││
││*gecos:                Masikh Masih                                         ││
││*sn:                   Masih                                                ││
││ homeDirectory:        /home/masikh                                         ││
││*automountInformation: -soft,intr,nosuid nfs-server04:/users/14/student:&   ││
││*cn:                   Masikh                                               ││
││                                                                            ││
│└─[Press [ESC] when done, [arrow keys] to select and [enter] to edit.]───────┘│
└──[Modify > User > Modify user attributes]────────────────────────────────────┘
```

Change each attribute you wish and press escape when done. MPLS
will ask you if you'd like to commit these changes. E.g.

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Modify user attributes                                                     ││
││                                                                            ││
││*employeeType:         Student                                              ││
││ uid:                  masikh                                               ││
││*loginShell:           /bin/bash                                            ││
││*uidNumber:            6929                                                 ││
││*employeeNumber:       500.6929                                             ││
││*gidNumber:            500                                                  ││
││*gecos:                Masikh Masih                                         ││
││*sn:                   Masih                                                ││
││ homeDirectory:        /home/masikh                                         ││
││*automountInformation: -soft,intr,nosuid nfs-server04:/users/14/student:&   ││
││*cn:                   Masikh                                               ││
││                                                                            ││
││ Do you wish to commit the changes? [y|n]                                   ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > User > Modify user attributes]────────────────────────────────────┘
```

'y' will commit the changes made.

__NOTE:__ An astrix * means a changed attribute.

### <a name="modifymenu-user-add-multiple" />-> User -> Add multiple users

With this helper you can add users in a batch process. You can
cut&paste a list of users from a text file into MPLS and create
these users in one blow.
The source file follows a strict format:

```bash
studentnumber:firstname:initials:preposition:surname

E.g. 1292285:Andrada:A.I.::Bacaoanu
```

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

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add users                                                                  ││
││                                                                            ││
││ File format: studentnumber:firstname:initials:preposition:surname          ││
││                                                                            ││
││ e.g.: 1046853:Ran:R.::An                                                   ││
││       1286781:Emmanuel:E.:A:Appiah                                         ││
││       1292285:Andrada:A.I.::Bacaoanu                                       ││
││       . <- End of file marker!!!                                           ││
││                                                                            ││
││ Paste file contents here: 2 lines pasted, 0 lines discarded.               ││
││┌──────────────────────────────────────────────────────────────────────────┐││
│││                                                                          │││
│││                                                                          │││
│││12345123:Robert:RDA::Nagtegaal                                            │││
│││12342132:Dirk:DS::Stoop                                                   │││
│││.                                                                         │││
││└──────────────────────────────────────────────────────────────────────────┘││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > User > Add multiple users]────────────────────────────────────────┘
```
After this two questions about employeeType and
automountInformation will be asked:

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add users                                                                  ││
││                                                                            ││
││*employeeType:         Guest                                                ││
││*automountInformation: -soft,intr,nosuid nfs-server02:/users/15/student:&   ││
││                                                                            ││
│└─[Press [ESC] when done, [arrow keys] to select and [enter] to edit.]───────┘│
└──[Modify > User > Add multiple users]────────────────────────────────────────┘
```

Press escape when all is filled in correctly. A do you which to
commit question will be asked. E.g.

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add users                                                                  ││
││                                                                            ││
││*employeeType:         Gast                                                 ││
││*automountInformation: -soft,intr,nosuid nfs-server06:/users/15/student:&   ││
││                                                                            ││
││ Ready to add 2 users, do you wish to continue? [y|n]                       ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > User > Add multiple users]────────────────────────────────────────┘

```

Finally you'll be asked if you wish to print the new account-forms
on a CUPS printer of your choice (Highly recommended to answer
yes!!!)

__Example:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Print account form                                                         ││
││                                                                            ││
││ Queue               Location                                               ││
││────────────────────────────────────────────────────────────────────────────││
││ ISSC_P2202_17       Snellius, kamer 47, PAND 2202                          ││
││ ISSC_P2202_19       Snellius, kamer 47, PAND 2202                          ││
││ ISSC_P2202_20       Snellius, kamer 40, PAND 2202                          ││
││ ISSC_P2202_24       Snellius, kamer 404, PAND 2202                         ││
││ ISSC_P2202_33       Snellius, kamer 56, PAND 2202                          ││
││ hp-106-bw           Snellius, kamer 106, PAND 2202                         ││
││ hp-119-bw           Snellius, kamer 119, PAND 2202                         ││
││ hp-123-c            Snellius, kamer 123, PAND 2202                         ││
││ hp-144-c            Snellius, kamer 144, PAND 2202                         ││
││ hp-145-c            Snellius, kamer 145, PAND 2202                         ││
││ hp-153-bw           Snellius, kamer 153, PAND 2202                         ││
││ hp-155-bw           Snellius, kamer 155, PAND 2202                         ││
││                                                                            ││
│└─[Usage: [ESC] quits, [arrows] select printer, [enter] use selected printer]┘│
└──[Modify > User > Add multiple users]────────────────────────────────────────┘
```

### <a name="modifymenu-group" />Modify -> Group

In this submenu you can add or delete a group, modify group
properties. You can also add or delete a user to/from a group.

### <a name="modifymenu-group-addgroup" />-> Group -> Add new group

With this helper you can add a new group to the LDAP database. A
group is either a primairy or secundairy group.
	
NOTE: If you add a primairy group make sure you reflect these
changes in the MPLS environment file also. See chapter
'Configuring MPLS for your environment'

If you try to add an existing group, an error is reported.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add new group                                                              ││
││                                                                            ││
││ Enter group:    csdale                                                     ││
││ Is this group a primairy group?: [y/n]                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > Group > Add new group]────────────────────────────────────────────┘
```

__Result:__

'OK' or 'Group csdale already exist!'

### <a name="modifymenu-group-delgroup" />-> Group -> Delete group

With this helper you can remove a group from the LDAP database. If
you deleted the wrong group the undo feature (transaction logs)
will enable you to fully revert that transaction. With fully is
ment, re-add the group PLUS its group-members.

__Example usage:__
```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Delete group                                                               ││
││                                                                            ││
││ Enter group:    csdale                                                     ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Modify > Group > Delete group]─────────────────────────────────────────────┘
```
__Result:__

'OK' or 'No such group'

### <a name="modifymenu-group-modgroup" />-> Group -> Modify group

With this helper you can modify group attributes. These attributes
are: cn (the group name), gidNumber and the group password.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Modify group attributes                                                    ││
││                                                                            ││
││ Enter group:    csdale                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > Group > Modify group]─────────────────────────────────────────────┘
```

In a new screen you can change the group attributes: e.g.

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Modifying group csdale                                                     ││
││                                                                            ││
││ cn                csdale                                                   ││
││ gidNumber         11158                                                    ││
││ userPassword      {crypt}*                                                 ││
││                                                                            ││
│└─[Use [ESC] when done or to quit, [arrow] selects item, [enter] modify item]┘│
└──[Modify > Group > Modify group]─────────────────────────────────────────────┘
```

If you're content with the modifications, press escape and commit
the changes by answering 'y' on the question 'Do you wish to
commit changes? [y|[n]]'.

__NOTE:__ This transaction is logged and revertable

### <a name="modifymenu-group-adduser" />-> Group -> Link user to group

With this helper you can add a user to a group.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Link user to group                                                         ││
││                                                                            ││
││ Enter username: masikh                                                     ││
││ Enter group:    csdale                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > Group > Link user to group]───────────────────────────────────────┘
```
__Result:__

'OK' or 'User masikh already in group csdale'

### <a name="modifymenu-group-deluser" />-> Group -> Unlink user from group

With this helper you can remove a user from a group

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Unlink user from group                                                     ││
││                                                                            ││
││ Enter username: masikh                                                     ││
││ Enter group:    csdale                                                     ││
││                                                                            ││
│└────────────────────────────────────────────────────────────────────────────┘│
└──[Modify > Group > Unlink user from group]───────────────────────────────────┘
```

__Result:__

'OK' or 'User masikh is not a member of group csdale!'

### <a name="modifymenu-netgroup" />Modify -> Netgroup

In this submenu you can add or delete a netgroup. Furthermore you
can add or remove an entity from a netgroup. An entity is either a
user, host or netgroup itself.

### <a name="modifymenu-netgroup-addgroup" />-> Netgroup -> Add new netgroup

With this helper you can add a new netgroup to the LDAP database.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Add new netgroup                                                           ││
││                                                                            ││
││ Enter netgroup: lgm                                                        ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Modify > Netgroup > Add new netgroup]──────────────────────────────────────┘
```

__Result:__

'netgroup lgm created' or 'ERROR: netgroup lgm already exists!'

### <a name="modifymenu-netgroup-delgroup" />-> Netgroup -> Delete netgroup

With this helper you can remove a netgroup from the LDAP
database. 

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Delete netgroup                                                            ││
││                                                                            ││
││ Enter netgroup: lgm                                                        ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Modify > Netgroup > Delete netgroup]───────────────────────────────────────┘
```

__Result:__

'OK' or 'ERROR: netgroup lgm does not exists!'

### <a name="modifymenu-netgroup-linkuser" />-> Netgroup -> Link entity to netgroup -> User to netgroup

With this helper you can add a user to a netgroup.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Link user to netgroup                                                      ││
││                                                                            ││
││ Enter username: masikh                                                     ││
││ Enter netgroup: users-sil                                                  ││
││                                                                            ││
││ ERROR: user masikh does not exists!                                        ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Modify > Netgroup > Link entity to netgroup > User to netgroup]────────────┘
```

__Result:__

'OK' or 'ERROR: netgroup users-sil does not exists!' or 'ERROR:
user masikh does not exists!'

### <a name="modifymenu-netgroup-linkhost" />-> Netgroup -> Link entity to netgroup -> Host to netgroup

With this helper you can add a hostname to a netgroup.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Link host to netgroup                                                      ││
││                                                                            ││
││ Enter hostname: stoeidoos                                                  ││
││ Enter netgroup: sil                                                        ││
││                                                                            ││
││ OK                                                                         ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Modify > Netgroup > Link entity to netgroup > Host to netgroup]────────────┘
```
__Result:__

'OK' or 'ERROR: netgroup sil does not exists!'

### <a name="modifymenu-netgroup-linkgroup" />-> Netgroup -> Link entity to netgroup -> Netgroup to netgroup

With this helper you can add a netgroup to a netgroup (Yes,
recursion!) It gives you the possibility to nest netgroups. This
reduces the amount of netgroups needed to run you business.

__Example usage:__

```bash
┌──────────────────────────────────────────────────────────────────────────────┐
│    Search           Modify           Login           Help           Exit     │
│────────────────────┌─────────────┐───────────────────────────────────────────│
│┌────────────────────────────────────────────────────────────────────────────┐│
││                                                                            ││
││ Link netgroup to netgroup                                                  ││
││                                                                            ││
││ Enter parent netgroup: silver                                              ││
││ Enter child netgroup:  stoeidoos                                           ││
││                                                                            ││
│└─[Press any key to continue]────────────────────────────────────────────────┘│
└──[Modify > Netgroup > Link entity to netgroup > Netgroup to netgroup]────────┘
```

__Result:__

'OK' or 'ERROR: netgroup .... does not exist!'

### <a name="modifymenu-netgroup-unlinkuser" />-> Netgroup -> Unlink entity to netgroup -> User to netgroup
### <a name="modifymenu-netgroup-unlinkhost" />-> Netgroup -> Unlink entity to netgroup -> Host to netgroup
### <a name="modifymenu-netgroup-unlinkgroup" />-> Netgroup -> Unlink entity to netgroup -> Netgroup to netgroup

## <a name="loginmenu" />Login Menu
## <a name="helpmenu" />Help Menu
## <a name="exit" />Exit Menu
## <a name="environment" />Configuring MPLS for your environment (uidNumber ranges, etc...)
## <a name="whatis" />What is a 'user', 'group' or 'netgroup' anyway?

__UNIX user__:

UNIX is a multiuser system. This means that separate users can
work simultaneously on the same hardware. In order to distinct
between these users, the concept of a username is devised.
A username is a way to identify which files or processes belongs
to who.

__UNIX group__:

When many users exist on a system it becomes hard to see which
role each user has. There might be staff members, guests etc..
The group concept is a convenient way to differentiate between
types of users. For instance you can make the groups 'staff',
'students' and 'guest' and place users in their respective group.
In this way it's much more easy to distinguish between users.

__UNIX netgroup__:

A netgroup defines a network-wide group of hosts and users. Use a
netgroup to restrict access to shared NFS file systems and to
restrict remote login and shell access.

Network groups are stored in a network information services, such
as LDAP, NIS, or NIS+, NOT in a local file.

## <a name="gpl" />About the Author/Programmer and Copyrights

|              |                                                        |
|:-------------|:-------------------------------------------------------|
|Author:       | Robert Nagtegaal                                       |
|E-mail:       | robert@liacs.nl, masikh@gmail.com                      |
|Copyright:    | Copyright 2013 Robert Nagtegaal                        |
|              | Robert Nagtegaal <masikh@gmail.com>                    |
|              | This program is distributed under the terms of the GNU |   
|              | General Public License (or the Lesser GPL)             |
|              |                                                        |
|Thanks to:    | Maartje Mulder (For putting up with all my absence)    |
|              | Kristian Rietveld (Teaching python)                    |
|              | Mattias Holm (Advice)                                  |
|              | Maarten Derickx (Advice)                               |
