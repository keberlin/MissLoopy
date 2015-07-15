#!/usr/bin/python

import argparse, csv

import psycopg2, database2

from utils import *
from iputils import *

parser = argparse.ArgumentParser(description='Create IP Address Database.')
parser.add_argument('file', nargs='+', help='a file for conversion')
args = parser.parse_args()

db = database2.Database(IP_ADDRESS_PG)

db.execute('DROP TABLE IF EXISTS tmp')
db.execute('CREATE TABLE tmp (lower BIGINT NOT NULL, upper BIGINT NOT NULL, country VARCHAR)')
db.execute('DROP INDEX idx1')
db.execute('CREATE UNIQUE INDEX idx1 ON tmp (lower, upper)')
db.commit()

# Load the country code data

countries = {}
with open('CountryCodes.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
  for row in reader:
    countries[row[0]] = row[1].decode('utf-8','ignore')
# Add special cases
countries['Europe'] = 'Europe'
countries['Asia'] = 'Asia'

# Load the ip/geo data

for file in args.file:
  print 'Processing', file,
  count = 0
  with open(file,'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
    for row in reader:
      try:
        db.execute('INSERT INTO tmp (lower,upper,country) VALUES(%s,%s,%s)' % (row[0], row[1], Quote(countries[row[2]])))
        db.commit()
        count += 1
      except psycopg2.IntegrityError:
        db.rollback()
        pass
      except Exception as e:
        print str(e), row
        db.rollback()
        pass
  print 'added', count, 'entries'

# Rename table

db.execute('DROP TABLE ranges')
db.execute('ALTER TABLE tmp RENAME TO ranges')
db.execute('CREATE INDEX idx2 ON ranges (lower)')
db.execute('CREATE INDEX idx3 ON ranges (upper)')
db.commit()
