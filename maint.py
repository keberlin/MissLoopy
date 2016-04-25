#!/usr/bin/python

import database, re

from utils import *
from gazetteer import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT * FROM profiles')
for entry in db.fetchall():
  db.execute('UPDATE profiles SET country=%s WHERE id=%d' % (Quote(GazCountry(entry[COL_LOCATION])), entry[COL_ID]))

db.commit()
