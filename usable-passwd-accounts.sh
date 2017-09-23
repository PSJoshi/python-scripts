#!/bin/sh

#Ref - http://www.cyberciti.biz/tips/search-for-all-account-without-password-and-lock-them.html

#passwd -S {user-name}

#-S : Display account status information. The status information consists of total seven fields. The second field indicates the status of password using following format:

#    L : if the user account is locked (L)
#    NP : Account has no password (NP)
#    P: Account has a usable password (P)

USERS="$(cut -d: -f 1 /etc/passwd)"
for u in $USERS
do
passwd -S $u | grep -Ew "P" >/dev/null
if [ $? -eq 0 ]; then
echo $u
fi
done
