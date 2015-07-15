#!/usr/bin/python

import csv, database

from utils import *
from mlutils import *
from emails import *

from logger import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT LOWER(email) FROM profiles WHERE verified')
emails = set([(entry[0]) for entry in db.fetchall()])

ids = []
with open('listed_email_365.txt', 'rb') as csvfile:
  reader = csv.reader(csvfile, quoting=csv.QUOTE_NONE, skipinitialspace=True)
  for row in reader:
    email = row[0].decode('utf-8', 'ignore').lower()
    if email in emails:
      db.execute('SELECT id FROM profiles WHERE email ILIKE %s LIMIT 1' % (Quote(email)))
      entry = db.fetchone()
      ids.append((entry[0], email))

for id, email in ids:
  DeleteMember(id)
  EmailKickedStopForumSpam(email)
  logger.info('Kicked %d %s' % (id, email))
