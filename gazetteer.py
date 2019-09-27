import os, math, difflib, re

import database

from utils import *

GAZETTEER_DB = 'gazetteer'

CIRCUM_X = 40075017
CIRCUM_Y = 40007860

def GazLatAdjust(y):
  return math.cos(y*2*math.pi/CIRCUM_Y)

def GazLocation(location):
  db = database.Database(GAZETTEER_DB)

  db.execute('SELECT x,y,tz FROM locations WHERE location=%s LIMIT 1' % (Quote(location)))
  return db.fetchone()

def Alias(query):
  str = re.sub(r'\W',r'',query).lower()
  if str == 'us' or str == 'usa' or str == 'america':
    return 'United States'
  if str == 'uk' or str == 'britain':
    return 'United Kingdom'
  if str == 'uae':
    return 'United Arab Emirates'
  if str == 'rwp':
    return 'Rawalpindi'
  return None

def GazClosestMatchesQuick(query,max):
  db = database.Database(GAZETTEER_DB)

  alias = Alias(query)
  if alias:
    query = alias

  closest = []

  db.execute('SELECT location FROM locations WHERE location ILIKE %s ORDER BY population DESC LIMIT %d' % (Quote(query+'%'), max))
  closest.extend([(entry[0]) for entry in db.fetchall()])
  if len(closest) < max:
    db.execute('SELECT location FROM locations WHERE location ILIKE %s ORDER BY population DESC LIMIT %d' % (Quote('%'+query+'%'), max))
    for entry in db.fetchall():
      if entry[0] not in closest:
        closest.append(entry[0])

  return closest[:max]

def GazClosestMatches(query,max):
  db = database.Database(GAZETTEER_DB)

  alias = Alias(query)
  if alias:
    query = alias

  closest = []

  db.execute('SELECT location FROM locations WHERE location ILIKE %s ORDER BY population DESC LIMIT %d' % (Quote('%'+query+'%'), max))
  closest.extend([(entry[0]) for entry in db.fetchall()])

  if len(closest) < max:
    db.execute('SELECT DISTINCT LOWER(SUBSTR(location,1,%d)) FROM locations' % (min(len(query),15)))
    locations = [(entry[0]) for entry in db.fetchall()]

    matches = difflib.get_close_matches(query, locations, max)
    # TODO remove any consecutive entries that are a subset of their preceding entry, e.g. Brugge, Brugg

    for match in matches:
      db.execute('SELECT location FROM locations WHERE location ILIKE %s ORDER BY population DESC LIMIT %d' % (Quote(match+'%'), max))
      for entry in db.fetchall():
        if entry[0] not in closest:
          closest.append(entry[0])
      if len(closest) >= max:
        break

  if len(closest) < max:
    db.execute('SELECT location FROM locations ORDER BY population DESC LIMIT %d' % (max))
    for entry in db.fetchall():
      if entry[0] not in closest:
        closest.append(entry[0])

  return closest[:max]

def GazPlacename(location1,location2):
  if not location1:
    return None
  s1 = location1.split(', ')
  s2 = location2.split(', ')
  n1 = len(s1)
  n2 = len(s2)
  i = 1
  while i < n1 and i < n2 and s1[n1-i] == s2[n2-i]:
    i += 1
  return ', '.join(s1[0:n1-i+1])

def GazCountry(location):
  s = location.split(', ')
  return s[-1]
