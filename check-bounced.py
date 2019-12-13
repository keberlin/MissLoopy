import csv, database

from utils import *
from mlutils import *

bounced = set()
with open('bounced.log', 'r') as f:
  for email in f.readlines():
    bounced.add(email)

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT LOWER(email) FROM profiles WHERE verified')
emails = set([(entry[0]) for entry in db.fetchall()])

for email in emails.intersection(bounced):
  print 'Bounced email address %s is registered' % (email)
  db.execute('SELECT id,name,location,last_ip FROM profiles WHERE email ILIKE %s LIMIT 1' % (Quote(email)))
  print ' ', db.fetchone()
