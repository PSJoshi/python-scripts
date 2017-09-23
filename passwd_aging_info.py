#!/usr/bin/env python
import subprocess
import logging
import sys
"""
Ref - http://www.cyberciti.biz/faq/linux-howto-check-user-password-expiration-date-and-time/
$ chage -l user_name
Last password change					: Jan 10, 2012
Password expires					: never
Password inactive					: never
Account expires						: never
Minimum number of days between password change		: 0
Maximum number of days between password change		: 99999
Number of days of warning before password expires	: 7

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
password_never_expires_accounts = 0
password_inactive_accounts = 0
account_never_expires = 0
password_change_min_days = list()
password_change_max_days = list()
password_warning_days = list()

for user in user_list:
	#logger.debug(user)
	cmd = ['sudo','/usr/bin/chage','-l',user]
	logger.info("Password information for the user - %s" %user)
	res=subprocess.Popen(cmd,stdout=subprocess.PIPE)
	result=res.communicate()[0]
	passwd_info = result.strip()#.split('\n')
	logger.info(passwd_info)
	password_response=passwd_info.split('\n')
	for item in password_response:
		if item.lower().find("password expires")>=0:
			if "never" in item.split(":")[1]:
				password_never_expires_accounts += 1
		if item.lower().find("account expires")>=0:
			if "never" in item.split(":")[1]:
				account_never_expires += 1
		if item.lower().find("password inactive")>=0:
			if "never" in item.split(":")[1]:
				password_inactive_accounts += 1
		if item.lower().find("minimum number of days")>=0:
			password_change_min_days.append(item.split(":")[1])

		if item.lower().find("maximum number of days")>=0:
			password_change_max_days.append(item.split(":")[1])

		if item.lower().find("number of days of warning")>=0:
			password_warning_days.append(item.split(":")[1])

print password_never_expires_accounts,account_never_expires
print max(password_change_min_days),max(password_change_max_days)
print max(password_warning_days)


