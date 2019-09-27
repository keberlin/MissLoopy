#!/usr/bin/python

import sys

from mlparse import *

for line in sys.stdin.readlines():
  dob = line.strip()
  dt = ParseDob(dob)
  if not dt:
    print dob
