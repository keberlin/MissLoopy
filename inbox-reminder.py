#!/usr/bin/python

import os

import database

from mlutils import *
from emails import *

db = database.Database(MISS_LOOPY_DB)

now = datetime.datetime.utcnow()
since = now-datetime.timedelta(days=14)

db.execute('SELECT DISTINCT(p.id) FROM profiles AS p INNER JOIN emails AS e ON p.id=e.id_to WHERE NOT e.viewed AND e.sent<%s' % (Quote(str(since))))
ids = map(lambda(x):int(x[0]), db.fetchall())

for id in ids:
  db.execute('SELECT email, name FROM profiles WHERE id=%d LIMIT 1' % (id))
  entry = db.fetchone()
  email = entry[0]
  name  = entry[1]
  EmailInboxReminder(email, name)
