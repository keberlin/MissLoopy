import re, datetime, json, time
import requests

from utilities import *
from postcode import *
from geolocate import *

import database

SERVER_KEY='AIzaSyCYd-rpKMmESJv6Ry3Vr6M7fI92dK0duzA'

db = database.Database('scheduler')

def mkkey(beg,end): return beg+'-'+end

def fetch(beg,end):
  print 'geotravel:', mkkey(beg,end)
    
  lat1,lng1 = geolocate(beg)
  lat2,lng2 = geolocate(end)
    
  url = 'https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&region=uk&key=%s' % (str(lat1)+','+str(lng1),str(lat2)+','+str(lng2), SERVER_KEY)
  
  delay = 0
  while True:
    if delay:
      print 'geotravel: Waiting %d seconds..' % (delay)
      time.sleep(delay)
      delay *= 2
      if delay > 1*60*60:
        delay = 1*60*60
    else:
      delay = 1
    try:
      r = requests.get(url)
      if r.status_code != 200:
        print 'ERROR: Status code %s getting directions for %s' % (r.status_code, mkkey(beg,end))
        continue
      data = json.loads(r.text)
      status = data['status']
      if status != 'OVER_QUERY_LIMIT':
        break
    except:
      pass
  if status != 'OK':
    raise Exception('ERROR: Could not get directions for %s, status %s' % (mkkey(beg,end), status))
  seconds = 0
  for leg in data['routes'][0]['legs']:
    seconds += leg['duration']['value']
  distance = 0
  for leg in data['routes'][0]['legs']:
    distance += leg['distance']['value']
    
  return seconds, distance
    
geotravels = {}
sql = "SELECT start,destination,travelling_time,distance FROM geotravel ORDER BY modified"
db.execute(sql)
for entry in db.fetchall():
  beg = entry[0]
  end = entry[1]
  geotravels[mkkey(beg,end)] = (entry[2], entry[3] if entry[3] else 0)
  geotravels[mkkey(beg,end)] = (entry[2], entry[3] if entry[3] else 0)
print 'geotravels:', len(geotravels)
  
def geotravel(beg,end,accurate=False):
  # Ensure each postcode is valid
  if not postcode_valid(beg):
    raise Exception('ERROR: postcode not valid %s' % beg)
  if not postcode_valid(end):
    raise Exception('ERROR: postcode not valid %s' % end)
    
  if not accurate:
    # Just use the postcode outcodes
    beg = beg.split()[0]
    end = end.split()[0]
  
  if beg == end:
    return 0, 0
    
  v = geotravels.get(mkkey(beg,end))
  if v:
    return v
  v = geotravels.get(mkkey(end,beg))
  if v:
    return v
    
  seconds, distance = fetch(beg,end)
    
  now = datetime.datetime.utcnow()
  modified = str(now)

  sql = "INSERT INTO geotravel (start,destination,travelling_time,distance,modified) VALUES (%s,%s,%s,%s,%s)" % (Quote(beg), Quote(end), str(seconds), str(distance), Quote(modified))
  db.execute(sql)
  db.commit()
    
  geotravels[mkkey(beg,end)] = (seconds, distance)
  geotravels[mkkey(end,beg)] = (seconds, distance)
  
  return seconds, distance

def geotravel_update(n):
  sql = "SELECT start,destination FROM geotravel ORDER BY modified LIMIT %d" % (n)
  db.execute(sql)
  for entry in db.fetchall():
    beg = entry[0]
    end = entry[1]
    
    seconds, distance = fetch(beg,end)
      
    now = datetime.datetime.utcnow()
    modified = str(now)

    sql = "UPDATE geotravel SET travelling_time=%s,distance=%s,modified=%s WHERE start=%s AND destination=%s" % (str(seconds), str(distance), Quote(modified), Quote(beg), Quote(end))
    db.execute(sql)
    db.commit()

