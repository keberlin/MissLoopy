#!/usr/bin/python

from mlutils import *

import database

db = database.Database(MISS_LOOPY_DB)

i = 0
while True:
  try:
    i += 1
    print 'trying to insert (%d)..' % (i)
    db.execute('INSERT INTO photos (id) VALUES (1)')
    print 'worked'
    db.execute('SELECT LASTVAL()')
    print db.fetchone()
    break
  except:
    print '..didn''t work'
