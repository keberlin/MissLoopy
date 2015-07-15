#!/usr/bin/python

import database

from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute('UPDATE admin SET last_dump_member_search="2000-01-01 00:00:00"')
db.commit()
