#!/usr/bin/python

import database, re

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT * FROM profiles')
for entry in db.fetchall():
  db.execute('UPDATE profiles SET email=%s WHERE id=%d' % (Quote(re.sub(' +','',entry[COL_EMAIL])), entry[COL_ID]))

db.commit()
