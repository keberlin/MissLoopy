#!/usr/bin/python

import csv

with open('CountryCodes.csv','wb') as csvfile:
  writer = csv.writer(csvfile, delimiter=',')
  with open('GeoLite2-Country-Locations.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
    first = True
    for row in reader:
      if first:
	first = False
	continue
      if row[4] and row[5]:
        writer.writerow([row[4], row[5]])
