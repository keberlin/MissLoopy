import database

from mlutils import *
from emails import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT email,id FROM profiles WHERE not verified')
for entry in db.fetchall():
  print entry[0].encode('utf-8'), entry[1]
  EmailVerify(entry[0], entry[1])
