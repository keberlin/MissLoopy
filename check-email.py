#!/usr/bin/python

import sys

from mlparse import *

for line in sys.stdin.readlines():
  email = line.strip()
  dt = ParseEmail(email)
  if not dt:
    print email
