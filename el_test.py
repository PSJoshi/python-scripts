#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import random
import string

from random import randrange
from pprint import pprint
# import Python's JSON library for its loads() method
import json

# import time for its sleep method
from time import sleep

# import the datetime libraries datetime.now() method
from datetime import datetime

# use the Elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers

# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("http://localhost:9200")

# generate dummy values
N=10
my_list= list()
for i in range(5):
    my_dict = dict()
    rand_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    #my_dict = {"str field": "test string", "int field": randrange(100), "bool field": True}
    my_dict = {"str field": rand_string, "int field": randrange(100), "bool field": True}
    my_list.append(my_dict)
pprint(my_list)

# write test data to file
with open("test.json",'w',encoding = 'utf-8') as f:
   json.dump(my_list,f)
   # json.dump(my_list, f, ensure_ascii=False, indent=4)

# read test data from file
with open("test.json",'r') as f:
    data=json.load(f)

print("loading from file")
pprint(data)

doc_list = list()
# use Python's enumerate() function to iterate over list of doc strings
for num, doc in enumerate(data):

# catch any JSON loads() errors
    try:
        dict_doc = dict()
        # prevent JSONDecodeError resulting from Python uppercase boolean
        #doc = doc.replace("True", "true")
        #doc = doc.replace("False", "false")
        # convert the string to a dict object
        #dict_doc = json.loads(doc)
        dict_doc = doc 
        # add a new field to the Elasticsearch doc
        dict_doc["timestamp"] = datetime.now()

        # add a dict key called "_id" if you'd like to specify an ID for the doc
        dict_doc["_id"] = num

        # append the dict object to the list []
        doc_list += [dict_doc]
    except json.decoder.JSONDecodeError as err:
        # print the errors
        print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)

print ("Dict docs length:", len(doc_list))
print("Elastic format - documents")
pprint(doc_list)


# attempt to index the dictionary entries using the helpers.bulk() method
try:
    print ("\nAttempting to index the list of docs using helpers.bulk()")

    # use the helpers library's Bulk API to index list of Elasticsearch docs
    # Elastic < 6.0
    #resp = helpers.bulk(client, doc_list, index = "test_index",doc_type = "_doc")
    # Elastic > 6.0
    resp = helpers.bulk(client, doc_list, index = "test_index")
    # print the response returned by Elasticsearch
    print ("helpers.bulk() RESPONSE:", resp)
    print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

except Exception as err:

    # print any errors returned with helpers.bulk() API call
    print("Elasticsearch helpers.bulk() ERROR:", err)

# Check the results:
#result = client.count(index="test_index")
#print(result.body['count']) 
 
# get all of docs for the index
# Result window is too large, from + size must be less than or equal to: [100]
query_all = {
'size' : 100,
'query': {
'match_all' : {}
}
}

print ("\nSleeping for a few seconds to wait for indexing request to finish.")
sleep(2)

# pass the query_all dict to search() method
resp = client.search(
index = "test_index",
body = query_all
)
pprint(resp)
#print ("search() response:", json.dumps(resp, indent=4))
result=resp['hits']['hits']
#import pdb
#pdb.set_trace()
results = []
for hit in result:
    results.append(hit['_source'])
pprint(results)    
# print the number of docs in index
print ("Length of docs returned by search():", len(resp['hits']['hits']))
 

