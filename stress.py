#!/usr/bin/python

import random, database

from utils import *
from gazeteer import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)
db2 = database.Database(GAZETTEER_DB)

db2.execute('SELECT MIN(x),MIN(y),MAX(x),MAX(y) FROM locations')
x_min,y_min,x_max,y_max = db2.fetchone()

now = datetime.datetime.utcnow()
n = 500000
for i in range(1,n+1):
  x = random.randint(x_min,x_max)
  y = random.randint(y_min,y_max)
  name = 'Fake ' + str(i)
  email = 'fake' + str(i) + '@fake.com'
  dob = datetime.date(random.randint(now.year-99,now.year-18),random.randint(1,12),random.randint(1,28))
  gender = 1<<random.randint(0,1)
  ethnicity = 1<<random.randint(0,6)
  gender_choice = 1<<random.randint(0,1)
  ethnicity_choice = 1<<random.randint(0,6)
  db.execute('INSERT INTO profiles (created2,verified,x,y,name,email,dob,gender,ethnicity,gender_choice,ethnicity_choice) VALUES (' + Quote(str(now)) + ',1,' + str(x) + ',' + str(y) + ',' + Quote(name) + ',' + Quote(email) + ',' + Quote(str(dob)) + ',' + str(gender) + ',' + str(ethnicity) + ',' + str(gender_choice) + ',' + str(ethnicity_choice) + ')')
  if i%(n/100) == 0:
      print 'Processed ' + str(i*100/n) + '%..\r',
db.commit()
