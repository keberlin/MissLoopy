#!/usr/bin/python

import database

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

now = datetime.datetime.utcnow()

# Count online users (active within the last hour)
db.execute('SELECT COUNT(*) FROM profiles WHERE verified AND last_login>=%s' % (Quote(str(now-datetime.timedelta(hours=1)))))
entry = db.fetchone()
print 'Users online: %d' % entry[0]
