#!/usr/bin/python

import re

from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute("SELECT DISTINCT id_from,message FROM emails WHERE message NOT LIKE 'data:image/%%'")
for entry in db.fetchall():
  id_from = entry[0]
  message = re.sub('[\r\n]+',' ',entry[1])
  print '%d %s' % (id_from, message.encode('utf-8'))
