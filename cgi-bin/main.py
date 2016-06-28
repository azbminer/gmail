#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import string
import cgi
import glob
import os
import sys
import os
from time import gmtime, strftime
import cgitb
import base64
cgitb.enable()
print 'content-type: text/html'
parms = cgi.FieldStorage()
if 'param1' in parms.keys():
    print 'has param1 <h>\n'
    print parms.getvalue('param1') + '\n'
filesFound = []
print os.getcwd()
os.chdir('.')
print os.getcwd()
os.chdir('gimages')
dir = os.getcwd()
os.chdir(dir)

for file in glob.glob('*.jpg'):
    filesFound.append(file)
f = open('index.template', 'rb')
print filesFound
for l in f:
    if 'REPLACE_ME_1' in l:
        for g in filesFound:
            data_uri = open(g, 'rb').read().encode('base64'
                    ).replace('\n', '')
            img_tag = '<img src="data:image/png;base64,%s">' % data_uri

            print img_tag
    elif 'REPLACE_ME_2' in l:
        print strftime('%Y\xc2\xad%m\xc2\xad%d %H:%M:%S', gmtime())
    else:
        print l
