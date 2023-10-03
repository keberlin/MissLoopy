import argparse
import csv
import datetime

import psycopg2

import database
from gazetteer import *
from utils import *

parser = argparse.ArgumentParser(description='Create Geographical Gazetteer Information Database.')
parser.add_argument('file', nargs='+', help='a geographical file')
args = parser.parse_args()

db = database.Database(GAZETTEER_DB)

db.execute('DROP TABLE IF EXISTS tmp')
db.execute('CREATE TABLE tmp (location VARCHAR PRIMARY KEY NOT NULL, x INTEGER, y INTEGER, tz VARCHAR, population INTEGER)')
db.commit()

# Load locations data

countries = set()
locations = 0
for file in args.file:
  print 'Processing', file
  with open(file,'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE, skipinitialspace=True)
    for row in reader:
      try:
        db.execute('INSERT INTO tmp (location,x,y,tz,population) VALUES(%s,%d,%d,%s,%d)' % (Quote(row[0].decode('utf-8')), int(row[1]), int(row[2]), Quote(row[3]), int(row[4])))
        db.commit()
        countries.add(GazCountry(row[0]))
        locations += 1
      except psycopg2.IntegrityError as e:
        print str(e), row
        db.rollback()

print 'Countries : %5d' % (len(countries))
print 'Locations : %5d' % (locations)

# Rename table

db.execute('BEGIN')
db.execute('DROP INDEX IF EXISTS idx1')
db.execute('DROP TABLE locations')
db.execute('ALTER TABLE tmp RENAME TO locations')
db.execute('CREATE INDEX idx1 ON locations (location)')
db.commit()
