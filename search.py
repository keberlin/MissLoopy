import os, math, database

from utils import *
from tzone import *
from gazetteer import *
from mlutils import *

MAX_MATCHES = 300

def search2(distance,order,id,x,y,tz,gender,age,ethnicity,height,weight,gender_choice,age_min,age_max,ethnicity_choice,height_min,height_max,weight_choice):
  db = database.Database(MISS_LOOPY_DB)

  adjust = GazLatAdjust(y)

  rules = []
  rules.append('verified')
  rules.append('last_ip_country = country')
  # Only list profiles which match this person's selection criteria
  if distance:
    dx = distance*1000/adjust # Distance is stored in the db as metres so *1000
    dy = distance*1000
    rules.append('x BETWEEN %d AND %d' % (x-dx, x+dx))
    rules.append('y BETWEEN %d AND %d' % (y-dy, y+dy))
  rules.append('(gender & %d)!=0' % (gender_choice))
  if age_min:
    now = datetime.datetime.utcnow()
    ref = Datetime(now, tz)
    dob = datetime.date(ref.year-age_min,ref.month,ref.day)
    rules.append('dob <= %s' % (Quote(str(dob))))
  if age_max:
    now = datetime.datetime.utcnow()
    ref = Datetime(now, tz)
    dob = datetime.date(ref.year-age_max-1,ref.month,ref.day)
    rules.append('dob > %s' % (Quote(str(dob))))
  if ethnicity_choice:
    rules.append('(ethnicity & %d)!=0' % (ethnicity_choice))
  if height_min:
    rules.append('(height IS NULL OR height >= %d)' % (height_min))
  if height_max:
    rules.append('(height IS NULL OR height <= %d)' % (height_max))
  if weight_choice:
    rules.append('(weight IS NULL OR (weight & %d)!=0)' % (weight_choice))
  # Only list profiles which match the other member's selection criteria
  rules.append('(gender_choice IS NULL OR (gender_choice & %d)!=0)' % (gender))
  rules.append('(age_min IS NULL OR age_min <= %d)' % (age))
  rules.append('(age_max IS NULL OR age_max >= %d)' % (age))
  if ethnicity:
    rules.append('(ethnicity_choice IS NULL OR (ethnicity_choice & %d)!=0)' % (ethnicity))
  if height:
    rules.append('(height_min IS NULL OR height_min <= %d)' % (height))
    rules.append('(height_max IS NULL OR height_max >= %d)' % (height))
  if weight:
    rules.append('(weight_choice IS NULL OR (weight_choice & %d)!=0)' % (weight))
  criteria = ' AND '.join(rules)
  order_by = ''
  if order:
    if order == 'age':
      order_by = 'ORDER BY dob DESC'
    elif order == 'login':
      order_by = 'ORDER BY last_login DESC'
    elif order == 'created':
      order_by = 'ORDER BY created2 DESC'
    else:
      pass # Order must be by distance

  list = []
  db.execute('SELECT * FROM profiles WHERE %s %s LIMIT %d' % (criteria, order_by, MAX_MATCHES))
  for entry in db.fetchall():
    i = entry[COL_ID]
    dx = abs(x-entry[COL_X])*adjust/1000
    dy = abs(y-entry[COL_Y])/1000
    d = math.sqrt((dx*dx)+(dy*dy))
    if distance and d > distance:
      continue
    list.append((i,d))
  if order == 'distance':
    list.sort(cmp=lambda a,b:int(a[1]-b[1])) # TODO

  return map(lambda x:x[0], list)
