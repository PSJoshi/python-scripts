#!/usr/bin/env python
import requests
import sys
# track http to https redirects using python request library
response = requests.get('http:// github.com',allow_redirects=False)
print r.url
print r.status_code
# this will print [<Response [301]>] as github redirects all http urls to https urls
print r.history

