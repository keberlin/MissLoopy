#!/usr/bin/python

import sys, database

from utils import *
from mlutils import *

id = int(sys.argv[1])

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT last_ip,email,name FROM profiles WHERE id=%d LIMIT 1' % (id))
entry = db.fetchone()
if entry:
  ip = entry[0]
  email = entry[1]
  name = entry[2]
  messages = []
  db.execute("SELECT DISTINCT message FROM emails WHERE id_from=%d" % (id))
  for entry in db.fetchall():
    messages.append(entry[0])
  db.execute('SELECT COUNT(DISTINCT id_to) FROM emails WHERE id_from=%d' % (id))
  entry = db.fetchone()
  members = entry[0]
  str = '%d: %d, %s, %s, "%s", "%s"' % (id, members, ip, email, name, str(messages))
  print str.encode('utf8')
