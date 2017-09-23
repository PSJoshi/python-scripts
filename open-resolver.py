#!/usr/bin/env python
import requests
import logging
from bs4 import BeautifulSoup
from IPy import IP
import argparse
import sys

def validate_ip(ip_address):
    valid = True
    try:    
        IP(ip_address)
    except Error:
        valid = False
    return valid

# logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser('This script checks if the ip address is acting as Open recursive resolver for DNS queries using http://openresolver.com')
        parser.add_argument('--ip',dest='ip',help = 'Please enter ip address')
        args = parser.parse_args()
        if args.ip:
            ip_address = args.ip
        else:
            ip_address = None
        if not (ip_address and validate_ip(ip_address)) :
            logger.error("Please enter valid ip address and then try again. Exiting...")
            sys.exit(1)
        logger.info("Checking if ip address %s is acting as open recursive resolver" %ip_address)
        r = requests.get('http://openresolver.com/?ip=%s' %ip_address)
        soup = BeautifulSoup(r.text,'html.parser')
        result = soup.find('h2')
        logger.info(result.text)
    except Exception as e:
	logger.error("Error while checking whether ip address %s is acting as Open recursive resolver for DNS queries - %s" %(ip_address,e.message),exc_info=True)

