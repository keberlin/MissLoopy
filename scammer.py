#!/usr/bin/python

import os, sys, tempfile

BASE_DIR = os.path.dirname(__file__)

data = sys.stdin.read()

(fd,filename) = tempfile.mkstemp(dir=os.path.join(BASE_DIR, 'static', 'scammers'), prefix='scammer-', suffix='.msg')
with os.fdopen(fd, 'w') as f:
  f.write(data)
  f.close()
  os.chmod(filename,0444)
