import sys, csv

import database

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

print 'Dumping profiles..'
with open('profiles.csv', 'wb') as output:
  writer = csv.writer(output)
  db.execute('SELECT * FROM profiles')
  for entry in db.fetchall():
    fields = map(lambda x:x.encode('utf-8') if isinstance(x,unicode) else x,entry)
    writer.writerow(fields)

print 'Dumping photos..'
with open('photos.csv', 'wb') as output:
  writer = csv.writer(output)
  db.execute('SELECT * FROM photos')
  for entry in db.fetchall():
    fields = map(lambda x:x.encode('utf-8') if isinstance(x,unicode) else x,entry)
    writer.writerow(fields)

print 'Dumping emails..'
with open('emails.csv', 'wb') as output:
  writer = csv.writer(output)
  db.execute('SELECT * FROM emails')
  for entry in db.fetchall():
    fields = map(lambda x:x.encode('utf-8') if isinstance(x,unicode) else x,entry)
    writer.writerow(fields)

print 'Dumping blocked..'
with open('blocked.csv', 'wb') as output:
  writer = csv.writer(output)
  db.execute('SELECT * FROM blocked')
  for entry in db.fetchall():
    fields = map(lambda x:x.encode('utf-8') if isinstance(x,unicode) else x,entry)
    writer.writerow(fields)

print 'Dumping favorites..'
with open('favorites.csv', 'wb') as output:
  writer = csv.writer(output)
  db.execute('SELECT * FROM favorites')
  for entry in db.fetchall():
    fields = map(lambda x:x.encode('utf-8') if isinstance(x,unicode) else x,entry)
    writer.writerow(fields)

print 'Dumping results..'
with open('results.csv', 'wb') as output:
  writer = csv.writer(output)
  db.execute('SELECT * FROM results')
  for entry in db.fetchall():
    fields = map(lambda x:x.encode('utf-8') if isinstance(x,unicode) else x,entry)
    writer.writerow(fields)

print 'Dumping admin..'
with open('admin.csv', 'wb') as output:
  writer = csv.writer(output)
  db.execute('SELECT * FROM admin')
  for entry in db.fetchall():
    fields = map(lambda x:x.encode('utf-8') if isinstance(x,unicode) else x,entry)
    writer.writerow(fields)
