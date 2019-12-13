import time, datetime, database

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT id_from,COUNT(DISTINCT id_to),COUNT(*),MIN(sent) FROM emails GROUP BY id_from ORDER BY COUNT(DISTINCT id_to)')
for entry in db.fetchall():
  id_from = entry[0]
  members = entry[1]
  if members < 5:
    continue
  count = entry[2]
  sent_min = datetime.datetime(*time.strptime(entry[3],"%Y-%m-%d %H:%M:%S.%f")[:6])
  sent_max = datetime.datetime.utcnow()
  td = sent_max-sent_min
  seconds = td.days*24*60*60 + td.seconds
  frequency = seconds/count
  td = datetime.timedelta(seconds=frequency)
  print 'id:%d has sent %d messages to %d members, 1 every %s' % (id_from, count, members, TimeDiff(td))
