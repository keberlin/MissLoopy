import random

from database import GAZETTEER_DB_URI, MISSLOOPY_DB_URI, db_init
from gazeteer import *
from mlutils import *
from utils import *

session1 = db_init(MISSLOOPY_DB_URI)
session2 = db_init(GAZETTEER_DB_URI)

session2.execute('SELECT MIN(x),MIN(y),MAX(x),MAX(y) FROM locations')
x_min,y_min,x_max,y_max = session2.fetchone()

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
  session1.execute('INSERT INTO profiles (created2,verified,x,y,name,email,dob,gender,ethnicity,gender_choice,ethnicity_choice) VALUES (' + Quote(str(now)) + ',1,' + str(x) + ',' + str(y) + ',' + Quote(name) + ',' + Quote(email) + ',' + Quote(str(dob)) + ',' + str(gender) + ',' + str(ethnicity) + ',' + str(gender_choice) + ',' + str(ethnicity_choice) + ')')
  if i%(n/100) == 0:
      print 'Processed ' + str(i*100/n) + '%..\r',
session1.commit()
