import json
import urllib

import requests

import database
from postcode import *
from utilities import *

SERVER_KEY='AIzaSyCYd-rpKMmESJv6Ry3Vr6M7fI92dK0duzA'

db = database.Database('scheduler')

def fetch(postcode):
  print 'geolocate:', postcode
    
  #url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&region=uk&key=%s' % (urllib.quote(postcode+', UK'), SERVER_KEY)
  url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&region=uk' % (urllib.quote(postcode))
  
  delay = 0
  while True:
    if delay:
      print 'geolocate: Waiting %d seconds..' % (delay)
      time.sleep(delay)
      delay *= 2
      if delay > 1*60*60:
        delay = 1*60*60
    else:
      delay = 1
    try:
      r = requests.get(url)
      if r.status_code != 200:
        raise Exception('ERROR: Status %s getting location for %s' % (r.status_code, postcode))
      data = json.loads(r.text)
      status = data['status']
      if status != 'OVER_QUERY_LIMIT':
        break
    except:
      pass
  if status != 'OK':
    raise Exception('ERROR: Could not geocode %s, status %s' % (postcode, data['status']))
  location = data['results'][0]['geometry']['location']
  lat = location['lat']
  lng = location['lng']
  
  return lat, lng
  
geolocates = {}
sql = "SELECT location,lat,lng FROM geolocate"
db.execute(sql)
for entry in db.fetchall():
  geolocates[entry[0]] = (entry[1],entry[2])
print 'geolocates:', len(geolocates)

def geolocate(postcode):
  # Ensure each postcode is valid
  if not postcode_valid(postcode):
    raise Exception('ERROR: postcode not valid %s' % postcode)
    
  v = geolocates.get(postcode)
  if v:
    return v
  
  lat, lng = fetch(postcode)
  
  sql = "INSERT INTO geolocate (location,lat,lng) VALUES (%s,%s,%s)" % (Quote(postcode), str(lat), str(lng))
  db.execute(sql)
  db.commit()
  
  geolocates[postcode] = (lat,lng)

  return lat, lng
