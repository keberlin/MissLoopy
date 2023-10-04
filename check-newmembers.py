import datetime

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from mlutils import *
from model import *
from utils import *

db = db_init(MISSLOOPY_DB_URI)

now = datetime.datetime.utcnow()
since = now-datetime.timedelta(days=30)

count = 0
entries = db.session.query(ProfileModel).filter(ProfileModel.verified.is_(True)).filter(ProfileModel.created2>=since).all()
for entry in entries:
  id              = entry.id
  name            = entry.name
  dob             = entry.dob
  location        = entry.location
  gender          = entry.gender
  ethnicity       = entry.ethnicity
  last_ip         = entry.last_ip
  last_ip_country = entry.last_ip_country

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
