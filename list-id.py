#!/usr/bin/python

import sys, database

from utils import *
from mlutils import *

email = sys.argv[1]

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT id FROM profiles WHERE email ILIKE %s' % (Quote(email)))
entry = db.fetchone()
if entry:
  id = entry[0]
  print id
