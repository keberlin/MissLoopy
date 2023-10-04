import argparse
import csv

from sqlalchemy import text

from database import IPADDRESS_DB_URI, db_init
from model import RangeModel

parser = argparse.ArgumentParser(description='Create IP Address Database.')
parser.add_argument('file', nargs='+', help='a file for conversion')
args = parser.parse_args()

session = db_init(IPADDRESS_DB_URI)

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
  print 'Processing %s..' % (file)
  count = added = 0
  with open(file,'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
    for row in reader:
      count += 1
      lower = int(row[0])
      upper = int(row[1])
      country = countries.get(row[2])
      if not country:
        print 'Unrecognised country code: %s' % row[2]
        continue

      entry = session.query(lower==lower,upper==upper,country==country).one_or_none()
      if not entry:
        print 'Missing: %d %d %s' % (lower,upper,country)
        session.query(RangeModel).filter(RangeModel.lower>=lower,RangeModel.upper<=upper).delete()
        range = RangeModel(lower=lower,upper=upper,country=country)
        session.add(range)
        session.commit()
        added += 1
        continue

  print '  processed', count, 'entries, added', added

# TODO Remove any entries which are no longer valid?
