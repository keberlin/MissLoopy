#!/usr/bin/python

import os, sys, tempfile

BASE_DIR = os.path.dirname(__file__)

data = sys.stdin.read()

(fd,filename) = tempfile.mkstemp(dir=os.path.join(BASE_DIR, '..', 'scammers'), prefix='scammer-', suffix='.msg')
f = os.fdopen(fd, 'w')
f.write(data)
f.close()
os.chmod(filename,0444)
