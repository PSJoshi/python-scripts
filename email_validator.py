#/usr/bin/env python
import smtplib
import dns.query
import dns.message
import dns.name
import argparse
import sys
import logging
import re

# logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

google_dns = '8.8.8.8'
# address to be used for SMTP MAIL FROM command
from_address = "test@malinator.com"
# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

def get_MX_server(domain):
    mx_record = None
    d=dns.name.from_text(domain)  
    #r=dns.message.make_query(d,dns.rdatatype.ANY)
    #r=dns.message.make_query(d,dns.rdatatype.A)
    r=dns.message.make_query(d,dns.rdatatype.MX)
    resp=dns.query.udp(r,google_dns) 
    for d in resp.answer[0]:                      
        #print d
        #print dir(d)
        #print d.preference,d.rdtype,d.rdclass,d.to_text()
        #print d.preference,d.rdtype,d.rdclass,d.to_text().split(' ')[1]
        mx_record = d.to_text().split(' ')[1]
        if mx_record:
            break
    return mx_record


parser = argparse.ArgumentParser()
parser.add_argument('--email',dest='email',help = 'Please enter "To" email address')
args = parser.parse_args()
if args.email:
    to_email = args.email
else:
    to_email = None

if not to_email:
    logger.error("Please enter valid 'To' email address. Quitting...")
    sys.exit(1)

match = re.match(regex,to_email)
if match == None:
    logger.error("Not a valid 'To' email address! Quitting...")
    sys.exit(1)
logger.info("Finding domain information")
domain = to_email.split('@')[1]
logger.info("Using domain - %s for DNS lookup" % domain)
mx_server = get_MX_server(domain) 
# SMTP lib setup (use debug level for full output)
email_server = smtplib.SMTP()
#email_server.set_debuglevel(0)

# Initiate SMTP conversation
email_server.connect(mx_server)
email_server.helo(email_server.local_hostname)
email_server.mail(from_address)
code, message = email_server.rcpt(to_email)
email_server.quit()

if code == 250:
    logger.info("Email account exists!")
else:
    logger.info("Email account does not exists.")

