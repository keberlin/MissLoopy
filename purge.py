#!/usr/bin/python

import database

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

now = datetime.datetime.utcnow()

# Delete any unverified profiles after 1 month
db.execute('DELETE FROM profiles WHERE not verified AND created2<%s' % (Quote(str(now-datetime.timedelta(days=30)))))
db.commit()

# Delete all emails older than 6 months
db.execute('DELETE FROM emails WHERE sent<%s' % (Quote(str(now-datetime.timedelta(days=30*6)))))
db.commit()
