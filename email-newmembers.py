#!/usr/bin/python

import datetime, database, search

from utils import *
from localization import *
from emails import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT last_new_member_search FROM admin LIMIT 1')
since = db.fetchone()[0]

now = datetime.datetime.utcnow()

results = {}

db.execute('SELECT * FROM profiles WHERE verified AND created2>=%s AND created2<%s' % (Quote(str(since)), Quote(str(now))))
for entry in db.fetchall():
  id               = entry[COL_ID]
  name             = entry[COL_NAME]
  email            = entry[COL_EMAIL]
  dob              = entry[COL_DOB]
  location         = entry[COL_LOCATION]
  x                = entry[COL_X]
  y                = entry[COL_Y]
  tz               = entry[COL_TZ]
  gender           = entry[COL_GENDER]
  age              = Age(entry[COL_DOB])
  ethnicity        = entry[COL_ETHNICITY]
  height           = entry[COL_HEIGHT]
  weight           = entry[COL_WEIGHT]
  gender_choice    = entry[COL_GENDER_CHOICE]
  age_min          = entry[COL_AGE_MIN]
  age_max          = entry[COL_AGE_MAX]
  ethnicity_choice = entry[COL_ETHNICITY_CHOICE]
  height_min       = entry[COL_HEIGHT_MIN]
  height_max       = entry[COL_HEIGHT_MAX]
  weight_choice    = entry[COL_WEIGHT_CHOICE]

  ids = search.search2(50,'distance',id,x,y,tz,gender,age,ethnicity,height,weight,gender_choice,age_min,age_max,ethnicity_choice,height_min,height_max,weight_choice)

  # Remove blocked members
  ids = filter(lambda x:not BlockedMutually(id,x), ids)

  for i in ids:
    if i not in results:
      results[i] = []
    results[i].append(id)

for id in results.keys():
  db.execute('SELECT * FROM profiles WHERE id=%d LIMIT 1' % (id))
  entry = db.fetchone()
  if not entry:
    continue
  notifications = entry[COL_NOTIFICATIONS]
  if not notifications & NOT_NEW_MEMBERS:
    EmailNewMembers(entry, results[id])

db.execute('UPDATE admin SET last_new_member_search=%s' % (Quote(str(now))))
db.commit()
