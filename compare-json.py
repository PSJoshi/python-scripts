#!/usr/bin/env python
import json
from jsondiff import diff

with open('hw.json') as f:
	json_data = f.read()
json_prev = json.loads(json_data)

with open('hw_new.json') as f:
	json_data = f.read()
json_new = json.loads('hw_new.json')

diff(json_prev,json_new)

