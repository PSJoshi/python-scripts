#!/usr/bin/env python
import sys
import subprocess
import argparse
from datetime import datetime
import tldextract

DOMAIN_EXPIRY = ["Registry Expiry Date","Expiration","Domain Expiration Date", "Expiration Date"]
DOMAIN_CREATION = ['Created On']
REGISTRAR = ["Registrar","Sponsoring Registrar"]

def extract_date(date_str):
    try:
         #return datetime.strptime(date_str,'%d-%b-%Y %H:%M:%S')
         return datetime.strptime(date_str,'%d-%b-%Y')
    except Exception,e:
        print "exception during date conversion - {}".format(e.message)

def whois_query(domain):
    try:
         p = subprocess.Popen(['whois',domain], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    except Exception,e:
        print "Error while getting whois records - {}".format(e.message)
    whois_data = p.communicate()[0]
    # cleanup whois data
    whois_data = [ele for ele in whois_data.splitlines() if ele != '']
    
    if whois_data:
         #don't consider initial comment for parsing 
         for line in whois_data[1:]:
             if any(expire_string in line for expire_string in DOMAIN_EXPIRY):
                  print line
                  date_str = line.split('Date:')[1].split(' ')[0].strip()
                  #print date_str
                  print extract_date(date_str)
             if any(registrar_string in line for registrar_string in REGISTRAR):
                  print line
                  print line.split(':')[1]
             if any(registrar_string in line for registrar_string in DOMAIN_CREATION):
                  print line
                  date_str = line.split(':')[1].split(' ')
                  print extract_date(date_str[0])
             

if __name__ == '__main__':
    domains = ['yahoo.co.in','barc.gov.in','google.co.in','bing.co.in']
    for domain in domains:
        print "Checking %s" %domain
        whois_query(domain)
    
