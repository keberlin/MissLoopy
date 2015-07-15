#!/usr/bin/python

import csv, database

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT LOWER(email) FROM profiles WHERE verified')
emails = set([(entry[0]) for entry in db.fetchall()])

with open('listed_email_365.txt', 'rb') as csvfile:
  reader = csv.reader(csvfile, quoting=csv.QUOTE_NONE, skipinitialspace=True)
  for row in reader:
    email = row[0].decode('utf-8', 'ignore').lower()
    if email in emails:
      print 'Scammer email address %s is registered' % (email)
      db.execute('SELECT id,name,location,last_ip_country,last_ip FROM profiles WHERE email LIKE %s LIMIT 1' % (Quote(email)))
      print ' ', db.fetchone()
