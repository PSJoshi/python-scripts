#!/usr/bin/env python
import string
from base64 import b64encode
import os
from sklearn.feature_extraction.text import CountVectorizer
from nltk import bigrams
from urlparse import urlparse
import validators
import tldextract

string_length = 10
random_string = os.urandom(string_length)
r_string = b64encode(random_string).decode('utf-8')

def count_consonents(my_str):
    consonants = set("bcdfghjklmnpqrstvwxyz")
    cnt = sum(1 for c in my_str if c in consonants)
    return cnt

def a_count_consonents(my_str):
    consonants = set("bcdfghjklmnpqrstvwxyz")
    cnt = sum(my_str.count(c) for c in consonants)
    return cnt

def count_vowels(my_str):
    vowels = "aeiouAEIOU"
    cnt = 0
#    for char in my_str:
#        if char in vowels:
#            cnt +=1
    cnt = sum(1 for char in my_str if char in vowels)
    return cnt

def find_ngrams(my_str, n):
    input_list = my_str.split()    
    return zip(*[input_list[i:] for i in range(n)])

def find_ngrams_scikit(my_str,n):
    if n <= 1:
        n = 1
    vectorizer = CountVectorizer(ngram_range=(1,n))
    analyzer = vectorizer.build_analyzer()
    return analyzer(my_str)

def find_nltk_bigrams(my_str):
    split_str = my_str.split()
    bigram_str = bigrams(split_str)    
    return [item for item in bigram_str]

def url_entropy():
    pass

def url_length():
    pass

def url_tokens(my_str):
    bag_of_words = ["/","?",".","=","-","_"," "]
    token_list = list()

    for token_char in bag_of_words:
        my_str_tokens = my_str.split(token_char)
        token_dict = dict()
        if my_str_tokens:
            #print "%s:%s" %(token_char,len(my_str_tokens))
            token_dict[token_char] = len(my_str_tokens)
            token_list.append(token_dict)
    return token_list

def is_hostname_ip():
    pass
def url_NS_servers():
    pass
def url_MX_servers():
    pass
def url_ASN_info():
    pass
def url_google_pagerank():
    pass
def url_host_countries():
    pass
def url_blacklist_virustotal():
    pass

def url_hostname_path_query(my_str):
    if validators.url(my_str,require_tld=True):
        parsed_uri = urlparse(my_str)
        return parsed_uri

def url_dot_count(my_str):
    if validators.url(my_str,require_tld=True):
        split_url = my_str.split("://")
        if len(split_url) == 1:
            return split_url[0].count('.')
        elif len(split_url) == 2:
            return split_url[1].count('.')
    else:
        raise ValueError("error while counting dots in url")
    
def url_slash_count(my_str):
    if validators.url(my_str,require_tld=True):
        split_url = my_str.split("://")
        if len(split_url) == 1:
            return split_url[0].count('/')
        elif len(split_url) == 2:
            return split_url[1].count('/')
    else:
        raise ValueError("error while counting dots in url")

def url_domains(my_str):
    result = tldextract.extract(my_str)
    return result

def url_contains_ipv4_addr(my_str):
    if validators.url(my_str,require_tld=True):
        parsed_uri = urlparse(my_str)
        if validators.ipv4(parsed_uri.netloc):
            return True,parsed_uri.netloc
        else:
            return False,parsed_uri.netloc
    else:
        return False, None

if __name__ == "__main__":

    #print count_consonents("this is my test message")
    #print a_count_consonents("this is my test message")
    #print count_consonents(r_string)
    #print count_vowels("this is a test")
    #print find_ngrams("this is a test",3)
    #print find_ngrams_scikit("this is a test", 3)
    #print find_nltk_bigrams("this is a test")
    #print url_tokens("www.naturenilai.com/form2/paypal/webscr.php?cmd= login")
    #print url_hostname_path_query('https://www.amazon.in/gp/yourstore/home?ie=UTF8&ref_=nav_cs_ys')
    #print url_domains('https://www.amazon.org.kg/gp/yourstore/home?ie=UTF8&ref_=nav_cs_ys')
    #print url_contains_ipv4_addr('https://www.amazon.org.kg/gp/yourstore/home?ie=UTF8&ref_=nav_cs_ys')
    #print url_contains_ipv4_addr('https://192.168.3.1/repos/joshi')
    #print url_dot_count('192.168.33.17/repos/joshi')
    print url_slash_count('http://192.168.3.1/repos/joshi/')
