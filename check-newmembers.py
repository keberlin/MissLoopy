import datetime, database

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT last_new_member_search FROM admin LIMIT 1')
since = db.fetchone()[0]

now = datetime.datetime.utcnow()

count = 0
db.execute('SELECT * FROM profiles WHERE verified AND created2>=%s AND created2<%s' % (Quote(str(since)), Quote(str(now))))
for entry in db.fetchall():
  id              = entry[COL_ID]
  name            = entry[COL_NAME]
  dob             = entry[COL_DOB]
  location        = entry[COL_LOCATION]
  gender          = entry[COL_GENDER]
  ethnicity       = entry[COL_ETHNICITY]
  last_ip         = entry[COL_LAST_IP]
  last_ip_country = entry[COL_LAST_IP_COUNTRY]

  out = u'id:%d (%s) %s %d (%s) %s (%s)' % (id, name, Gender(gender), Age(dob), dob, location, last_ip_country)
  print out.encode('utf-8')

  count += 1

if count:
  td = now-since
  seconds = td.days*24*60*60 + td.seconds
  td = datetime.timedelta(seconds=seconds/count)
  print '%d new members since %s, 1 every %s, %d per day' % (count, str(since), TimeDiff(td), count*24*60*60/seconds)
else:
  print 'No new members since %s' % (str(since))
