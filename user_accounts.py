#!/usr/bin/env python
import subprocess
import logging
import sys
"""
Ref - http://www.cyberciti.biz/tips/search-for-all-account-without-password-and-lock-them.html
Display account status information consists 7 fields:
login name,password status,min age, max age,warning period and inactivity period

Second field indicates if the user account has a locked password (L), has
no password (NP), or has a usable password (P). 
"""
logger = logging.getLogger(__name__)
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logger.addHandler(console)
logger.setLevel(logging.DEBUG)

cmd=['/usr/bin/cut','-d:','-f','1','/etc/passwd']
res=subprocess.Popen(cmd,stdout=subprocess.PIPE)
result=res.communicate()[0]
user_list = result.strip().split('\n')
locked_passwd = 0
no_passwd = 0
set_passwd = 0

for item in user_list:
	#logger.debug(item)
	cmd = ['sudo','/usr/bin/passwd','-S',item]
	res=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	result=res.communicate()[0]
	passwd_info = result.strip().split('\n')
	for info in passwd_info:
		user_passwd_info = info.split(' ')
		if user_passwd_info[1].lower() == 'l':
			locked_passwd = locked_passwd + 1
		elif user_passwd_info[1].lower() == 'np':
			no_passwd = no_passwd + 1
			logger.info("account with no password:%s" % info[0])
		elif user_passwd_info[1].lower() == 'p':
			set_passwd = set_passwd + 1

logger.info("Users accounts password information:\n Locked passwords-%s No-passwords-%s with-passwords-%s" %(locked_passwd,no_passwd,set_passwd))


